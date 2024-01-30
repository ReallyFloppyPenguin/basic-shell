# basic-shell

Hello, world!

I have developed a mini shell script based on Python,
it'd be really helpful to point out any issues on this
project at my [Github](https://github.com/potato-pack/basic-shell/)

Here's the [wiki](https://github.com/potato-pack/basic-shell/wiki)

## Remember
  * It is only basic
  so don't expect parallel processing
  or compiling or anything like that.


  * This is not intended for industrial use.

  * Also I am still developing this, meaning that
  somethings like the wiki are not currently implemented

  * There are also some (big) bugs!

  * And this is currently in beta stages (still in development)
  so it may still produce error messages!


## Basic Documentation
  First, install it.
  `pip install basicshell`

  ```
  import basicshell
  shell = basicshell.Shell()
  while True:
    shell.execute()
  ```

  This is how you basically use the shell,
  there are more ways to use the shell, such as
  using pipes and specifying your own shell
  command in the `execute` function. This is all in the [wiki](https://github.com/potato-pack/basic-shell/wiki)
