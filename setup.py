from cx_Freeze import setup, Executable
  
setup(name = "Stegnography" ,
      version = "1.0" ,
      description = "" ,
      executables = [Executable("main.py")],
      )
