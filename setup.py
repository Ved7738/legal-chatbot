from setuptools import find_packages, setup

setup(
    name='Generative AI Law Chatbot Project',
    version='0.0.0',
    description="A law Chatbot using Langchain",
    author='Vedant Jaiswar',
    author_email='vedty070@gmail.com',
    long_description=open('README.MD').read(),
    url = 'https://github.com/sameergit0/Law-Chatbot.git',
    packages=find_packages(),
    install_requires =[
        'sentence-transformers==4.0.1',
        'langchain==0.3.21',
        'langchain_community==0.3.20',
        'langchain_experimental==0.3.4',
        'langchain-pinecone==0.2.0',
        'pinecone-client==5.0.1',
        'langchain-groq==0.3.1',
        'flask==3.1.0',
        'pypdf==5.4.0',
        'python-dotenv==1.1.0',
        'gunicorn'
    ],
    classifiers=[                        
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Windows',
    ],
    python_requires='>=3.12.7'
)