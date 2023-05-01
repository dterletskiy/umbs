import os
import signal

import pfw.console
import pfw.shell
import pfw.os.signal

import umbs.builders.base
import umbs.builders.image.partition



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )

def do_build( builder ):
   builder.config( )
   builder.build( )
   builder.test( )

def do_clean( builder ):
   builder.clean( )



def signal_handler( signum, frame, *args, **kwargs ):
   kw_object = kwargs.get( "object", None )

   pfw.console.debug.warning( f"signal: {signum}" )
   if signal.SIGINT == signum:
      kw_object.deinit( )
# def signal_handler



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "image" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__user_name = None
      self.__user_password = None
      self.__user_uid = None
      self.__user_gid = None
      if "user" in self.__config:
         if "name" in self.__config["user"]:
            self.__user_name = self.__config["user"]["name"]
            if "hashed_password" in self.__config["user"]:
               self.__user_password = self.__config["user"]["hashed_password"]
            else:
               password = self.__config["user"].get( "password", self.__config["user"]["name"] )
               password_salt = self.__config["user"].get( "password_salt", self.__config["user"]["name"] )
               self.__user_password = pfw.linux.password.build_hashed_password( password, password_salt )
         self.__user_uid = self.__config["user"].get( "uid", None )
         self.__user_gid = self.__config["user"].get( "gid", None )

      self.__hostname = self.__config.get( "hostname", "HOSTNAME" )

      if "packages" in self.__config:
         def process_packages( data ):
            pkg = ""

            if isinstance( data, str ):
               pkg = data
            elif isinstance( data, list ) or isinstance( data, tuple ):
               for item in data:
                  pkg += " " + process_packages( item )
            elif isinstance( data, dict ):
               for key, value in data.items( ):
                  pkg += " " + process_packages( value )
            else:
               pfw.console.debug.error( f"unsupported data type: {type(data)}" )

            return pkg
         # def process_packages

         self.__packages = process_packages( self.__config["packages"] ).split( ' ' )

      if "image" in self.__config:
         self.__image_builder = umbs.builders.image.partition.Builder(
               self.__config["image"],
               root_dir = self.__root_dir,
               project_dir = self.__product_dir
            )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def config( self, **kwargs ):
      pass
   # def config

   def build( self, **kwargs ):
      self.__image_builder.pre_build( )
      self.__image_builder.do_build( )

      self.__target_dir = self.__image_builder.mount_point( )

      self.init( )

      self.pre_install( )
      self.install( )
      self.post_install( )
      self.create_user( )

      self.deinit( )

      self.__image_builder.post_build( )
   # def build

   def pre_install( self, **kwargs ):
      # Setup /etc/hostname
      command = f"echo '{self.__hostname}' > /etc/hostname"
      self.execute( command )

      # Setup /etc/hosts
      command = f"echo '127.0.0.1   localhost' > /etc/hosts"
      self.execute( command )
      command = f"echo '127.0.1.1   {self.__hostname}' >> /etc/hosts"
      self.execute( command )
      command = f"echo '' >> /etc/hosts"
      self.execute( command )
      command = f"echo '# The following lines are desirable for IPv6 capable hosts' >> /etc/hosts"
      self.execute( command )
      command = f"echo '::1         ip6-localhost ip6-loopback' >> /etc/hosts"
      self.execute( command )
      command = f"echo 'fe00::0     ip6-localnet' >> /etc/hosts"
      self.execute( command )
      command = f"echo 'ff00::0     ip6-mcastprefix' >> /etc/hosts"
      self.execute( command )
      command = f"echo 'ff02::1     ip6-allnodes' >> /etc/hosts"
      self.execute( command )
      command = f"echo 'ff02::2     ip6-allrouters' >> /etc/hosts"
      self.execute( command )

      # Setup /etc/fstab
      command = f"echo 'proc        /proc       proc     defaults             0     0' > /etc/fstab"
      self.execute( command )
      # command = f"echo '/dev/vda1   /boot       vfat     defaults             0     2' >> /etc/fstab"
      self.execute( command )
      # command = f"echo '/dev/vda2   /           ext4     defaults,noatime     0     1' >> /etc/fstab"
      self.execute( command )

      # Setup /etc/resolv.conf
      # Setup internet connectivity in chroot
      # /etc/resolv.conf is required for internet connectivity in chroot.
      # It will get overwritten by dhcp, so don't get too attached to it.
      command = f"echo 'nameserver 8.8.8.8' > /etc/resolv.conf"
      self.execute( command )
      command = f"echo 'nameserver 2001:4860:4860::8888' >> /etc/resolv.conf"
      self.execute( command )

      # Setup /etc/apt/sources.list
      # Setup apt source list
      command = "sed -i -e \"s/# deb /deb /\" /etc/apt/sources.list"
      self.execute( command, bash = False )

      # Configure /tmp directory
      command = f"chmod 1777 /tmp"
      self.execute( command, bash = False )

      # # Configure divert
      # command = f"dpkg-divert --local --rename --add /sbin/initctl"
      # self.execute( command )
      # command = f"ln -s /bin/true /sbin/initctl"
      # self.execute( command )
   # def pre_install

   def install( self, **kwargs ):
      # Update and upgrade packages
      self.execute( f"apt update" )
      self.execute( f"apt -y upgrade" )
      self.execute( f"apt autoremove -y" )
      self.execute( f"apt clean all" )

      # Install required packages
      for package in self.__packages:
         self.execute( f"apt install -y {package}", method = "system" )

      self.execute( f"apt autoremove -y" )
      self.execute( f"apt clean all" )
   # def install

   def post_install( self, **kwargs ):
      # Configure machine-id
      command = f"dbus-uuidgen > /etc/machine-id"
      self.execute( command )
      command = f"ln -fs /etc/machine-id /var/lib/dbus/machine-id"
      self.execute( command )

      # # Remove the diversion
      # command = f"rm /sbin/initctl"
      # self.execute( command )
      # command = f"dpkg-divert --rename --remove /sbin/initctl"
      # self.execute( command )
   # def post_install

   def create_user( self ):
      # Create user
      if self.__user_name:
         if self.__user_uid and self.__user_gid:
            command = f"groupadd --gid {self.__user_gid} {self.__user_name}"
            self.execute( command, bash = False )

         command = f"useradd --create-home --shell /bin/bash --groups adm,sudo --password {self.__user_password}"
         if self.__user_uid and self.__user_gid:
            command += f" --uid {self.__user_uid}"
            command += f" --gid {self.__user_gid}"
         command += f" {self.__user_name}"
         self.execute( command, bash = False )
   # def create_user

   def clean( self, **kwargs ):
      pass
   # def clean

   def init( self, **kwargs ):
      pfw.os.signal.add_handler( signal.SIGINT, signal_handler, object = self )

      # Mounting required host stuff
      pfw.shell.execute( f"sudo -S mount -o bind /proc {self.__target_dir}/proc", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S mount -o bind /dev {self.__target_dir}/dev", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S mount -o bind /dev/pts {self.__target_dir}/dev/pts", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S mount -o bind /sys {self.__target_dir}/sys", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S mount -o bind /tmp {self.__target_dir}/tmp", output = pfw.shell.eOutput.PTY )

      return True
   # def init

   def deinit( self, **kwargs ):
      # Unmounting required host stuff
      pfw.shell.execute( f"sudo -S umount {self.__target_dir}/tmp", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S umount {self.__target_dir}/sys", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S umount {self.__target_dir}/dev/pts", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S umount {self.__target_dir}/dev", output = pfw.shell.eOutput.PTY )
      pfw.shell.execute( f"sudo -S umount {self.__target_dir}/proc", output = pfw.shell.eOutput.PTY )

      pfw.os.signal.remove_handler( signal.SIGINT, signal_handler )
   # def deinit

   def execute( self, command: str, **kwargs ):
      kw_bash = kwargs.get( "bash", True )
      kw_method = kwargs.get( "method","subprocess" )

      if kw_bash:
         pfw.shell.execute( command, chroot_bash = self.__target_dir, method = kw_method, output = pfw.shell.eOutput.PTY )
      else:
         pfw.shell.execute( command, chroot = self.__target_dir, method = kw_method, output = pfw.shell.eOutput.PTY )
   # def execute
# class Builder
