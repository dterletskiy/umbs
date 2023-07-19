# umbs
Universal Meta Build System

- [Fetchers](./.md/fetchers/fetchers.md)



# ***Fetchers***



# ***Builders***

## ***cmake***

### ***common***

Required parameters:
- **type**: **cmake.common**
    - type: string
    - description: builder type
    - required value: **cmake.common**

Optional parameters:
- **subdirs**: *items*
    - type: map
    - description: ***relative to the project directory*** pathes used in current builder
    - items:
        - **target**:
            - type: string
            - description: ***relative to the project directory*** path where the source code and the main CMakeLists.txt file are located. This path is used as the value for '***-S***' parameter during calling ***cmake***.
            - default value: "."
        - **product**:
            - type: string
            - description: ***relative to the project directory*** path where the *all* build artifacts are located. This path is used as the value for '***-B***' parameter during calling ***cmake***.
            - default value: "."
        - **deploy**:
            - type: string
            - description: ***relative to the project directory*** path where the *final* build artifacts are located. This path is used for installation after build. This path is used as the value for '***--install-prefix***' parameter during calling ***cmake***.
            - default value: "."

- **graphviz**:
    - type: string
    - description: ***relative to the project directory*** path where the generated graphviz dependencies by ***cmake*** will be stored. This path is used as the value for '***--graphviz=***' parameter during calling ***cmake***.
    - default value: None (graphviz will not be generated)

- **jobs**:
    - type: integer
    - description: number of jobs for building. This value is used for '***-j***' parameter during calling ***cmake***
    - default value: None (parameter will not be used)

- **variables**:
    - type: list
    - description: list of the variables to be passed to the ***cmake***. Each item of this list is used as the value for '***-D***' parameter during calling ***cmake***. The syntax of each item must satisfy to cmake '***-D***' option rule (\<var\>[:\<type\>]=\<value\>)
    - default value: None

- **env**:
    - type: list
    - description: list of the environment variables to be set before calling the build.
    - default value: None

- **artifacts**:
    - type: list
    - description: ***relative to the project directory*** list of the files and directories what are defined as build artifacts and will be tested for existence after successfull build.
    - default value: None

- **deps**:
    - type: list
    - description: ***relative to the root directory*** list of the files and directories what are defined as the dependencies for current builder and will be tested for existence before the build.
    - default value: None





# ***Tools***
