# 🤖 csx-ssg - a static site generator

## 📄 Summary
This static site generator turns Markdown files into fully-fledged static pages.

It supports the standard Markdown syntax, such as:
- Headers,
- Links,
- Images,
- Lists,
- Quotes,
- Codeblocks,
- Text formatting,
- ... and anything else you'd expect from Markdown.


## 🛠 Requirements
- Python 3.9+
- A web browser


## 🚀 Usage & Demo
### 🌱 Quick start
- Clone this repository and `cd` into it.
- Run `main.sh` and go to `localhost:8888` in your browser. This is the project demo, which you may explore at your own leisure.

### 📝 Adding your content
- To add your own content, head to the `/content` directory and start adding Markdown files.
- To create paths and nest your content, add folders. For example, files added to `/content/my_page_path` will be accessible at `localhost:8888/my_page_path/file_name`.
- Static content such as stylesheets, images or videos should be added to the `/static` folder. You may reference these in your Markdown files. See sample usage in the sample provided in the `/content` directory.
- Once you're done, run the `main.sh` again. Your generated site should be in the `/public` directory.


## ⚠ Warning
This software was written and tested on **Linux**.
If you are a Windows user and run into problems, feel free to open an issue or
modify the source code yourself.
Pull requests are welcome.
