# Automatic Blog Post
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/built%20with-Python3-green.svg" alt="built with Python3" /></a>

Automatic blog post is a Python project created to generate automatically blog posts from videos.

<img src="images/architecture.png" alt="drawing" width="700"/>

The final blog post consists of 5 main parts: title, summary, image, text and keywords. The image above represents how this architecture works. As you can see, this is a natural language processing project.

First, we need to process the video to extract the audio. Using the DeepGram API we can do the speech to text. Later, we split the text into paragraphs. For that, we are analyzing the pause between the words to find if the sentences belong to the same paragraph or if it’s a new one.

Then, we use some pre-trained machine learning models to create the text keywords and summary. We also get the video thumbnail and name, which will be our blog post image and title, respectively.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install -r requirements.txt
```

## Usage

```python

```

## License
[Apache-2 license](https://www.apache.org/licenses/LICENSE-2.0)