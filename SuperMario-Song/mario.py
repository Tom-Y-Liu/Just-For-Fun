from wave import open
from struct import Struct
from math import floor

frame_rate = 11025

def encode(x):
    """Encode float x between -1 and 1 as two bytes.
    (See https://docs.python.org/3/library/struct.html)
    """
    i = int(16384 * x)
    return Struct('h').pack(i)

def play(sampler, name='song.wav', seconds=11):
    """Write the output of a sampler function as wav file.
    (See https://docs.python.org/3/library/wave.html)
    """
    out = open(name, 'wb')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(frame_rate)
    t = 0
    while t < seconds * frame_rate:
        sample = sampler(t)
        out.writeframes(encode(sample))
        t = t + 1
    out.close()

def tri(frequency, amplitude=0.3):
    """A continuous triangle wave."""
    period = frame_rate // frequency
    def sampler(t):
        saw_wave = t / period - floor(t / period + 0.5)
        tri_wave = 2 * abs(2 * saw_wave) - 1
        return amplitude * tri_wave
    return sampler

c_freq, d_freq, e_freq, f_freq, g_freq, a_freq, b_freq= 261.63, 293.665, 329.63, 349.228, 392.00, 440, 493.88

def both(f, g):
    return lambda t: f(t) + g(t)

def note(f, start, end, fade=0.01):
    def sampler(t):
        seconds = t / frame_rate
        if seconds < start:
            return 0
        elif seconds > end:
            return  0
        elif seconds <  start + fade:
            return (seconds - start) / fade * f(t)
        elif seconds > end -fade:
            return (end - seconds) / fade * f(t)
        else:
            return f(t)
    return sampler

def mario_at(octave):
    c, d, e, f = tri(octave * c_freq), tri(octave* d_freq), tri(octave * e_freq), tri(octave* f_freq)
    g, a, b = tri(octave * g_freq), tri(octave* a_freq), tri(octave * b_freq)
    low_c, low_d, low_e, low_f = tri(octave * c_freq/2), tri(octave * d_freq/2), tri(octave * e_freq/2), tri(octave * f_freq/2)
    low_g, low_a, low_b = tri(octave * g_freq/2), tri(octave * a_freq/2), tri(octave * b_freq/2)
    return mario(c, d, e, f, g, a, b, low_c, low_d, low_e, low_f, low_g, low_a, low_b)


def mario(c, d, e, f, g, a, b, low_c, low_d, low_e, low_f, low_g, low_a, low_b):
    z = 0
    song = note(e, z, z + 1/8)
    z += 1/8
    song = both(song, note(e, z, z + 1/8))
    z += 1/4
    song = both(song, note(e, z, z + 1/8))
    z += 1/4
    song = both(song, note(c, z, z + 1/8))
    z += 1/8
    song = both(song, note(e, z, z + 1/8))
    z += 1/2
    song = both(song, note(g, z, z + 1/4))
    z += 1/2
    song = both(song, note(low_g, z, z + 1/4))
    z += 1

    song = both(song, note(c, z, z + 1/4))
    z += 1/2
    song = both(song, note(low_g, z, z + 1/4))
    z += 1/2
    song = both(song, note(low_e, z, z + 1/4))
    z += 1/2
    song = both(song, note(low_a, z, z + 1/4))
    z += 1/2

    song = both(song, note(low_b, z, z + 1/4))
    z += 1/2
    song = both(song, note(tri(466.16), z, z + 1/4))
    z += 1/2
    song = both(song, note(low_a, z, z + 1/4))
    z += 1/2
    song = both(song, note(low_g, z, z + 1/4))
    z += 1/2
    song = both(song, note(e, z, z + 1/4))
    z += 1/2
    song = both(song, note(g, z, z + 1/8))
    z += 1/4
    song = both(song, note(a, z, z + 1/8))
    z += 1/4
    song = both(song, note(f, z, z + 1/8))
    z += 1/4
    song = both(song, note(g, z, z + 1/8))
    z += 1/4
    song = both(song, note(e, z, z + 1/4))
    z += 1/2
    song = both(song, note(c, z, z + 1/8))
    z += 1/8
    song = both(song, note(d, z, z + 1/8))
    z += 1/4
    song = both(song, note(low_b, z, z + 1/4))
    z += 1/2
    song = both(song, note(c, z, z + 1/4))
    z += 1/2
    song = both(song, note(low_g, z, z + 1/4))
    z += 1/2
    return song
play(mario_at(1))

# def test(c=tri(c_freq), d=tri(d_freq), e=tri(e_freq), f=tri(f_freq), g=tri(g_freq), a=tri(a_freq), b=tri(b_freq)):
#     z = 0
#     song = note(e, z, z + 1/2)
#     z += 1/2
#     song = both(song, note(e, z, z + 1/2))
#     z += 1/2
#     song = both(song, note(d, z, z + 1/2))
#     z += 1/2
#     song = both(song, note(e, z, z + 1/2))
#     z += 1/2
#     song = both(song, note(tri(1), z, z + 1/2))
#     z += 1/2
#     song = both(song, note(e, z, z + 1/2))
#     z += 1/2
#     song = both(song, note(g, z, z + 1/2))
#     z += 1/2
#     song = both(song, note(e, z, z + 1/2))
#     z += 1/2
#     song = both(song, note(d, z, z + 1/2))
#     z += 1/2
#     song = both(song, note(e, z, z + 1/2))
#     return song
# play(test())
