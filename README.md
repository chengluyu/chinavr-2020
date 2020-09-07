# Billow

Control particle-based fluid by your sound.

## Usage

1. Install packages: `pip install -r requirements.txt`.
2. Run the program: `python main.py`.

P.S. If microphone cannot be detected. Run `python main.py -l` to find the microphone ID.
Then run `python main.py -d <ID>` where `<ID>` is the microphone ID.

P.P.S. If you're using macOS (any version after Mojava), you should run it in Terminal.
Don’t do it in VSCode’s built-in terminal because it won’t ask for microphone permission.

## Credit

* The spectrum visualization code is from [`sounddevice`’s example](https://python-sounddevice.readthedocs.io/en/0.4.0/examples.html#real-time-text-mode-spectrogram).
* The 3D PBF code is from Taichi forum user [@lqxu](https://forum.taichi.graphics/t/homework2-3d-pbf/1102)’s [implementation](https://github.com/jackylovechina/taichidemo/blob/master/PBF_3D.py).

<details>
<summary>I'm very ashamed that I made such small contributions. 🌚</summary>
很惭愧，只做了一点微小的工作。
</details>
