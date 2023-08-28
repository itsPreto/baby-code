import re
import unittest

def detect_file_request(text):
    # Regular expression pattern to detect file paths
    pattern = r'(/[\w\-\.\/]+(?:\.\w+))'
    match = re.search(pattern, text)
    
    print(match.group(1))
    return match.group(1) if match else None

class TestDetectFileRequest(unittest.TestCase):

    def test_text_files(self):
        self.assertEqual(detect_file_request("Can you read /path/to/file.txt?"), "/path/to/file.txt")
        self.assertEqual(detect_file_request("What's in /documents/note.md?"), "/documents/note.md")
        self.assertEqual(detect_file_request("Summarize the contents of this file: /Users/marconeves/Downloads/shakespeare.txt"), "/Users/marconeves/Downloads/shakespeare.txt")

    def test_code_files(self):
        self.assertEqual(detect_file_request("What's the output if I run /projects/python/script.py?"), "/projects/python/script.py")
        self.assertEqual(detect_file_request("Debug /webpage/assets/script.js"), "/webpage/assets/script.js")
        self.assertEqual(detect_file_request("Check for errors in /code/main.c"), "/code/main.c")

    def test_data_files(self):
        self.assertEqual(detect_file_request("What's the data in /sheets/financials.xlsx?"), "/sheets/financials.xlsx")
        self.assertEqual(detect_file_request("Can you analyze /database/sample.sql?"), "/database/sample.sql")
        self.assertEqual(detect_file_request("Tell me the stats from /data/report.h5"), "/data/report.h5")

    def test_image_files(self):
        self.assertEqual(detect_file_request("How does /images/sample.jpg look?"), "/images/sample.jpg")
        self.assertEqual(detect_file_request("Is /profile/picture.png a good photo?"), "/profile/picture.png")
        self.assertEqual(detect_file_request("Display the image at /photos/vacation.tiff"), "/photos/vacation.tiff")

    def test_document_files(self):
        self.assertEqual(detect_file_request("What's the content of /reports/annual.pdf?"), "/reports/annual.pdf")
        self.assertEqual(detect_file_request("Show me the slides in /conference/presentation.ppt"), "/conference/presentation.ppt")
        self.assertEqual(detect_file_request("Read the first page of /documents/contract.docx"), "/documents/contract.docx")

    def test_audio_files(self):
        self.assertEqual(detect_file_request("Can I listen to /music/album/song.flac?"), "/music/album/song.flac")
        self.assertEqual(detect_file_request("Play the track from /audio/recordings/interview.m4a"), "/audio/recordings/interview.m4a")
        self.assertEqual(detect_file_request("What's the duration of /podcasts/episode1.mp3?"), "/podcasts/episode1.mp3")

    def test_video_files(self):
        self.assertEqual(detect_file_request("I'd like to watch /movies/adventure.mp4"), "/movies/adventure.mp4")
        self.assertEqual(detect_file_request("Preview the clip at /videos/sample.avi"), "/videos/sample.avi")
        self.assertEqual(detect_file_request("What's the resolution of /recordings/conference.webm?"), "/recordings/conference.webm")

    def test_archive_files(self):
        self.assertEqual(detect_file_request("What's inside /backup/data.rar?"), "/backup/data.rar")
        self.assertEqual(detect_file_request("List the contents of /archives/project.zip"), "/archives/project.zip")
        self.assertEqual(detect_file_request("Extract /compressed/files.tar.gz for me"), "/compressed/files.tar.gz")

    def test_other_files(self):
        self.assertEqual(detect_file_request("Can you mount /os/windows.iso?"), "/os/windows.iso")
        self.assertEqual(detect_file_request("What's the size of /backup/full.img?"), "/backup/full.img")

if __name__ == "__main__":
    unittest.main()