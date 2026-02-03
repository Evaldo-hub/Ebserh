from setuptools import setup, find_packages

setup(
    name="ebserh-ti-study",
    version="1.0.0",
    description="EBSERH TI Study App - Aplicativo de estudos para concurso",
    author="EBSERH TI Study Team",
    author_email="contact@ebserh-ti-study.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "Flask==3.0.0",
        "Jinja2==3.1.4",
        "gunicorn==23.0.0",
        "psycopg2-binary==2.9.10",
        "Pillow==10.4.0",
        "python-dotenv==1.0.1",
        "Werkzeug==3.0.3",
        "MarkupSafe==2.1.5",
        "itsdangerous==2.2.0",
        "click==8.1.7",
        "blinker==1.9.0",
    ],
    extras_require={
        "dev": [
            "pytest==8.3.0",
            "black==24.10.0",
            "flake8==7.1.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Flask",
    ],
)
