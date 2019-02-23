import main
from pytest import approx

def test_duration():

    ins = main.convert()
    names = ins.multiconvert()
    for name in names:
        induration, outduration = ins.ffprobe(name[0], name[1])
        assert induration == approx(outduration)
        induration, outduration = ins.ffprobe(name[0], name[2])
        assert induration == approx(outduration)

if __name__ == '__main__':
    test_duration()
