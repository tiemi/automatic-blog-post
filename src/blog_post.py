import os
import asyncio
import platform

import numpy as np
from transformers import pipeline
from keyphrase_vectorizers import KeyphraseCountVectorizer
from keybert import KeyBERT
from deepgram import Deepgram

class BlogPost():
    def __init__(self, video, output_directory):
        self.video = video
        self.text = None
        self.output_directory = output_directory

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def get_summary(self):
        print('Starting generating summary')
        text_summarizer = pipeline('summarization')
        summary = text_summarizer(
            self.get_text().replace('\n\n', '\n'),
            max_length=150,
            min_length=40
        )[0].get('summary_text')
        print('Finished generating summary')
        return summary

    def get_keywords(self, n):
        print('Starting generating keywords')
        keyword_model = KeyBERT()
        keywords = keyword_model.extract_keywords(
            docs=[self.get_text().replace('\n\n', '\n')],
            vectorizer=KeyphraseCountVectorizer()
        )
        if keywords:
            top_keywords = sorted(keywords[0], key=lambda t: t[1], reverse=True)[:n]
            processed_keywords = [f'#{keyword.replace(" ", "")}' for keyword, score in top_keywords]
        print('Finished generating keywords')
        return ' '.join(processed_keywords)

    def generate_markdown_post(self):
        mardown_template = '''# {title}\n\n\{keywords}\n\n{summary}\n\n<img src="{image_name}" width="700"/>\n\n{text}'''

        mardown_post = mardown_template.format(
            title=self.video.get_title(),
            summary=self.get_summary(),
            image_name=os.path.basename(self.video.get_image_path()),
            text=self.get_text(),
            keywords=self.get_keywords(3)
        )
        return mardown_post

    def save_markdown_post(self, mardown_post):
        print('Starting saving blog post')
        with open(self.get_md_path(), 'w', encoding='utf-8') as file:
            file.write(mardown_post)
        print('Finished saving blog post')

    def get_md_path(self):
        return os.path.join(self.output_directory, f'{self.video.get_base_name()}.md')

    def __split_paragraphs(self, transcript, time_difference_list):
        pause_list = [time_diff['time'] for time_diff in time_difference_list if time_diff['time'] > 0]
        median_pause = np.median(pause_list)
        processed_text = []
        paragraph = []
        min_paragraph_len = 30

        for ind, processed_word in enumerate(transcript['transcript'].split(' ')):
            time_diff = time_difference_list[ind]['time']

            if (time_diff <= median_pause * 1.5) and ((processed_word.islower()) or (len(paragraph) < min_paragraph_len)):
                paragraph.append(processed_word)
            else:
                paragraph.append(processed_word)
                processed_text.append(' '.join(paragraph))
                paragraph = []
        return '\n\n'.join(processed_text)

    def generate_text(self, deepgram_key):
        print('Starting generating text')
        dg_client = Deepgram(deepgram_key)
        if platform.system()=='Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        transcript = asyncio.run(self.__generate_transcript(dg_client))
        transcripted_words_list = transcript.get('words', [{}])
        time_difference_list = []
        for ind, transcripted_word in enumerate(transcripted_words_list[:-1]):
            time_difference_list.append(
                {
                    'index': ind,
                    'word': transcripted_word.get('word'),
                    'time': transcripted_words_list[ind+1].get('start') - transcripted_word.get('end')
                }
            )
        time_difference_list.append(
            {
                'index': ind+1,
                'word': transcripted_word.get('word'),
                'time': 0
            }
        )
        self.set_text(self.__split_paragraphs(transcript, time_difference_list))
        print('Finished generating text')

    async def __generate_transcript(self, dg_client):
        with open(self.video.get_audio_path(), 'rb') as audio:
            source = {'buffer': audio, 'mimetype': 'audio/wav'}
            response =  await dg_client.transcription.prerecorded(source, {'punctuate': True})
            transcript = response.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0]
        return transcript
