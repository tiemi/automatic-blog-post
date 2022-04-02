import argparse

from src.video import Video
from src.blog_post import BlogPost

def generate_blog_post(video_url, deepgram_key):
    output_directory = 'output'

    video = Video(video_url, output_directory)
    video.download_audio()
    video.download_image()
    blog_post = BlogPost(video, output_directory)
    await blog_post.generate_text(deepgram_key)
    markdown_post = blog_post.generate_markdown_post()
    blog_post.save_markdown_post(markdown_post)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '-v',
        '--video',
        action='store',
        dest='video_url',
        help='The Youtube video url'
    )
    parser.add_argument(
        '-dk',
        '--deepgram',
        action='store',
        dest='deepgram_key',
        help='The DeepGram API key'
    )

    args = parser.parse_args()

    generate_blog_post(
        video_url=args.video_url,
        deepgram_key=args.deepgram_key
    )
