from setuptools import find_packages, setup 

# This function returns a list of required packages for the project. It is called by the setup() function.
def get_requirements()->list[str]:
    requirements_list = list[str] =[]
    return requirements_list


setup(
    name='APS_Fault_Detection',
    version="0.0.1",
    author="keshavi",
    author_email="2k22.cse.2213443@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements() , 
)
