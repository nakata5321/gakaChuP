from web_parser.hashtag_parser import *
import sys

def main():
    post_link = 'https://www.instagram.com/p/B0glJybHOGS/'
    parser = HashTagParser(headless=False);
    hashfield = HashField();
    parser.signIn('gakachup', 'vladison99')
    time.sleep(5)

    parser.getHashTagMap(post_link, hashfield)
    hashfield.saveTree(sys.argv[1])
    print(hashfield.getHashTree())
    print(hashfield.getHashTable())


if __name__ == '__main__':
    main()
