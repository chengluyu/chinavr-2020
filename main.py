import math
import numpy as np
import taichi as ti
import sounddevice as sd
from audio import parse_args, create_gradient
from pbf import init_particles, scene, move_board, run_pdf, boundary


if __name__ == "__main__":
    parser, args, remaining = parse_args()
    low, high = args.range  # the frequency range

    # the color scale
    gradient = create_gradient()

    try:
        # let me have a look
        print('Color Scale', ''.join(gradient))

        # sample rate means how many samples are records per second
        samplerate = sd.query_devices(args.device, 'input')[
            'default_samplerate']

        # how much frequency that a column represents
        delta_f = (high - low) / (args.columns - 1)
        fftsize = math.ceil(samplerate / delta_f)
        low_bin = math.floor(low / delta_f)

        # the current value of highest magnitude
        highest_magnitude = 0

        def callback(indata, frames, time, status):
            global highest_magnitude
            if status:
                text = ' ' + str(status) + ' '
                print('\x1b[34;40m', text.center(args.columns, '#'),
                      '\x1b[0m', sep='')
            if any(indata):
                # the shape of indata is (sample_rate * block_duration / 1000, 1)
                # because `indata` is samples across time, we should use rfft
                # to get the samples across frequencey range
                magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
                magnitude *= args.gain / fftsize
                # here we only use elements from `low_bin` to `low_bin + columns`
                magnitude_slice = magnitude[low_bin:low_bin + args.columns]
                line = (gradient[int(np.clip(x, 0, 1) * (len(gradient) - 1))]
                        for x in magnitude_slice)
                highest_magnitude = np.max(magnitude_slice)
                print(*line, sep='', end='\x1b[0m\n')
            else:
                print('no input')

        with sd.InputStream(device=args.device, channels=1, callback=callback,
                            # how many samples should be read for each time
                            blocksize=int(
                                samplerate * args.block_duration / 1000),
                            samplerate=samplerate) as input_stream:
            init_particles()
            gui = ti.GUI('PBF_3D', scene.res)
            while gui.running:
                gui.running = not gui.get_event(ti.GUI.ESCAPE)
                if highest_magnitude > 0.2:
                    move_board(highest_magnitude * 10)
                run_pdf()
                scene.camera.set(pos=[boundary[0] / 2 + 1, 10, -40],
                                 target=[boundary[0] / 2 + 1, 5, 0],
                                 up=[0, 1, 0])
                scene.render()
                gui.set_image(scene.img)
                gui.show()
    except KeyboardInterrupt:
        parser.exit('Interrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
