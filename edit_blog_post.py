import argparse

from src.video import Video
from src.blog_post import BlogPost
from src.editor import read_process_dict, read_text, process_text

def edit_blog_post(video_url):
    output_directory = 'output'
    process_dict_path = 'input/process_dictionary.json'
    
    video = Video(video_url, output_directory)
    blog_post = BlogPost(video, output_directory)

    blog_post_path = blog_post.get_md_path()
    process_dict = read_process_dict(process_dict_path)
    text = read_text(blog_post_path)
    processed_text = process_text(text, process_dict)

    blog_post.set_text(processed_text)
    markdown_post = blog_post.generate_markdown_post()
    blog_post.save_markdown_post(markdown_post)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--video',
        action='store',
        dest='video_url',
        help='The Youtube video url'
    )

    args = parser.parse_args()
    edit_blog_post(args.video_url)
