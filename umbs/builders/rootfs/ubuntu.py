import os
import signal

import pfw.console
import pfw.shell
import pfw.os.signal

import umbs.builders.base
import umbs.builders.image.partition



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance



def signal_handler( signum, frame, *args, **kwargs ):
   kw_object = kwargs.get( "object", None )

   pfw.console.debug.warning( f"signal: {signum}" )
   if signal.SIGINT == signum:
      kw_object.deinit( )
# def signal_handler



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      strict_fields = [ "source" ]
      for key in strict_fields:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )


      self.__source = os.path.join( self.__target_dir, self.__config["source"] )

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

      self.__packages_apt = [ ]
      self.__packages_pip2 = [ ]
      self.__packages_pip3 = [ ]
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

         packages = self.__config["packages"]

         if "apt" in packages:
            self.__packages_apt = process_packages( packages["apt"] ).split( ' ' )

         if "pip2" in packages:
            self.__packages_pip2 = process_packages( packages["pip2"] ).split( ' ' )

         if "pip3" in packages:
            self.__packages_pip3 = process_packages( packages["pip3"] ).split( ' ' )

      self.__image_builder = None
      if "image" in self.__config:
         self.__image_builder = umbs.builders.image.partition.Builder(
               self.__config["image"],
               root_dir = self.__root_dir,
               project_dir = self.__product_dir
            )
   # def __init__

   def config( self, **kwargs ):
      return True
   # def config

   def build( self, **kwargs ):
      if not os.path.exists( self.__source ):
         pfw.console.debug.error( f"source image or directory for building roots does not exist: {self.__source}" )
         return False

      if os.path.isfile( self.__source ):
         self.__target_dir = pfw.linux.image.mount( self.__source )
         if not self.__target_dir:
            return False

      self.init( )

      self.__pre_install( )
      self.__install( )
      self.__post_install( )
      self.__create_user( )

      self.deinit( )

      if os.path.isfile( self.__source ):
         self.__target_dir = pfw.linux.image.umount( self.__source )

      return True
   # def build

   def __pre_install( self, **kwargs ):
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
   # def __pre_install

   def __install( self, **kwargs ):
      # Update and upgrade packages
      self.execute( f"apt update" )
      self.execute( f"apt -y upgrade" )

      # Install required apt packages
      for package in self.__packages_apt:
         self.execute( f"apt install -y {package}", method = "system" )

      # Install required pip2 packages
      for package in self.__packages_pip2:
         self.execute( f"pip2  install {package}", method = "system" )

      # Install required pip3 packages
      for package in self.__packages_pip3:
         self.execute( f"pip3 install {package}", method = "system" )

      self.execute( f"apt autoremove -y" )
      self.execute( f"apt clean all" )
   # def __install

   def __post_install( self, **kwargs ):
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
   # def __post_install

   def __create_user( self ):
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
   # def __create_user

   def clean( self, **kwargs ):
      return True
   # def clean

   def init( self, **kwargs ):
      pfw.os.signal.add_handler( signal.SIGINT, signal_handler, object = self )

      # Mounting required host stuff
      self.execute( f"sudo -S mount -o bind /proc {self.__target_dir}/proc" )
      self.execute( f"sudo -S mount -o bind /dev {self.__target_dir}/dev" )
      self.execute( f"sudo -S mount -o bind /dev/pts {self.__target_dir}/dev/pts" )
      self.execute( f"sudo -S mount -o bind /sys {self.__target_dir}/sys" )
      self.execute( f"sudo -S mount -o bind /tmp {self.__target_dir}/tmp" )

      return True
   # def init

   def deinit( self, **kwargs ):
      # Unmounting required host stuff
      self.execute( f"sudo -S umount {self.__target_dir}/tmp" )
      self.execute( f"sudo -S umount {self.__target_dir}/sys" )
      self.execute( f"sudo -S umount {self.__target_dir}/dev/pts" )
      self.execute( f"sudo -S umount {self.__target_dir}/dev" )
      self.execute( f"sudo -S umount {self.__target_dir}/proc" )

      pfw.os.signal.remove_handler( signal.SIGINT, signal_handler )
   # def deinit

   def execute( self, command: str, **kwargs ):
      kw_bash = kwargs.get( "bash", True )
      kw_method = kwargs.get( "method","subprocess" )

      result = None
      if kw_bash:
         result = self.execute( command, chroot_bash = self.__target_dir, method = kw_method )
      else:
         result = self.execute( command, chroot = self.__target_dir, method = kw_method )

      return 0 == result["code"]
   # def execute
# class Builder
