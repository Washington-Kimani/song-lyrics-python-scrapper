from mylyrics.azlyrics import AZLyrics
import argparse


parser = argparse.ArgumentParser(description="Scrape song's lyrics from several providers")
parser.add_argument("-a", "--artist", help="artist's name", required=True)
parser.add_argument("-s", "--song", help="song's name", required=True)


def main():

    args = parser.parse_args()

    artist = args.artist
    song = args.song

    s = AZLyrics(artist, song)
    lyrics = s.scrape()

    print(lyrics)


if __name__ == "__main__":

    main()