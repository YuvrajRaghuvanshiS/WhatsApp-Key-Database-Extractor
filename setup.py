import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wakdbe",  # Replace with your own username
    version="0.4.1",
    author="Yuvraj Raghuvanshi",
    author_email="YuvrajRaghuvanshi.S@protonmail.com",
    description="Extract WhatsApp key/DB from package directory (/data/data/com.whatsapp) without root access.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor",
    project_urls={
        "Bug Tracker": "https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=['wakdbe', 'wakdbe/bin', 'wakdbe/extracted',
              'wakdbe/helpers', 'wakdbe/non_essentials'],
    package_data={
        "": ["*.txt", ".placeholder", "bin/*"],
        "wakdbe": ["bin/*.*"],
    },
    python_requires=">=3.6",
)
