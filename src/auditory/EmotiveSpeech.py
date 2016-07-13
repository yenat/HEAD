from pyo import *
import numpy
import voiced_unvoiced as voi
import pitch_mark_first_step as pmfs
import pitch_mark_second_stage as pmss
from scipy.io import wavfile
import Inflection as inflect
import td_psola as psola

def emotiveSpeech(filename,typeOfEmotion):
    if typeOfEmotion == "Happy":
        sep = filename.split("/")
        name = sep[len(sep)-1].split(".")[0]
        print name
        filenameFreqShift = "Vocie-samples/" + str(name) + "FreqShiftHappy.wav"
        filenameInflection = "Vocie-samples/" + str(name) + "InflectionHappy.wav"
        filenameAverage = "Vocie-samples/" + str(name) + "AverageHappy.wav"
        filenameHappy = "Vocie-samples/" + str(name) + "Happy.wav"

        fs, x = wavfile.read(filename)
        x = voi.get_one_channel_array(x)
        chunk_size = 1024
        vSig = voi.get_signal_voiced_unvoiced_starting_info(x,fs,chunk_size)
        lengthVoiced = voi.get_signal_voiced_length_info(x,vSig)

        voiced_regions = voi.get_voiced_region_chunks(vSig,lengthVoiced)

        pitch_marks,voiced_region_freq_chunk_windows_pitch_marks_obj = pmfs.get_pitch_marks_regions(x,voiced_regions,chunk_size, "voiced")
        best_voiced_region_freq_chunk_windows_pitch_marks_obj = pmss.optimal_accumulated_log_probability(x,voiced_region_freq_chunk_windows_pitch_marks_obj)

        best_pitch_marks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["best_pitch_marks"]
        freq_chunks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["freq_chunks"]


        best_pitch_marks = []
        for best_pitch_marks_region in best_pitch_marks_info:
            for best_pitch_marks_freq_chunk in best_pitch_marks_region:
                for i in best_pitch_marks_freq_chunk:
                    best_pitch_marks.append(i)

        new_x = psola.freq_shift_using_td_psola_helper_new_two(x,best_pitch_marks,1.08)
        new_sndarray = []
        for i in range(0,len(new_x)):
            new_sndarray.append(numpy.int16(new_x[i]))

        new_sndarray = voi.make_two_channels(new_sndarray)
        voi.write_to_new_file(filenameFreqShift,numpy.asarray(new_sndarray))

        fs, xf = wavfile.read(filenameFreqShift)
        xf = voi.get_one_channel_array(xf)
        vSig = voi.get_signal_voiced_unvoiced_starting_info(xf,fs,chunk_size)
        lengthVoiced = voi.get_signal_voiced_length_info(xf,vSig)

        voiced_regions = voi.get_voiced_region_chunks(vSig,lengthVoiced)

        new_snd = inflect.inflection(xf,voiced_regions,0.5,fs,chunk_size)
        new_snd_new = []
        cnt = 0
        for i in new_snd:
            new_snd_new.append(numpy.int16(i))
            if cnt == len(new_snd)-1:
                break
            cnt = cnt + 1
        wavfile.write(filenameInflection,fs,numpy.array(new_snd_new))

        s = Server().boot()
        s.start()
        sf2 = SfPlayer(filenameInflection, speed=1, loop=False)
        dur = sndinfo(filenameInflection)[1]
        t3 = NewTable(length=dur)
        out2 = Average(sf2,200,mul=10).out()
        rec3 = TableRec(out2, table=t3)
        rec3.play()
        s.start()
        time.sleep(dur*4)
        s.stop()
        savefileFromTable(t3,filenameAverage,0,0)


        s.start()
        dur = sndinfo(filenameAverage)[1]
        sf = SfPlayer(filenameAverage, speed=1, loop=False)
        t2 = NewTable(length=dur)
        out = Atone(sf, 8000,mul=20).out()
        rec2 = TableRec(out, table=t2)
        rec2.play()
        s.start()
        time.sleep(dur*4)
        s.stop()

        savefileFromTable(t2,filenameHappy,0,0)
    if typeOfEmotion == "Sad":
        sep = filename.split("/")
        name = sep[len(sep)-1].split(".")[0]
        filenameFreqShift = "Vocie-samples/" + str(name) + "FreqShiftSad.wav"
        filenameSad = "Vocie-samples/" + str(name) + "Sad.wav"

        fs, x = wavfile.read(filename)
        x = voi.get_one_channel_array(x)
        chunk_size = 1024
        vSig = voi.get_signal_voiced_unvoiced_starting_info(x,fs,chunk_size)
        lengthVoiced = voi.get_signal_voiced_length_info(x,vSig)

        voiced_regions = voi.get_voiced_region_chunks(vSig,lengthVoiced)

        pitch_marks,voiced_region_freq_chunk_windows_pitch_marks_obj = pmfs.get_pitch_marks_regions(x,voiced_regions,chunk_size, "voiced")
        best_voiced_region_freq_chunk_windows_pitch_marks_obj = pmss.optimal_accumulated_log_probability(x,voiced_region_freq_chunk_windows_pitch_marks_obj)

        best_pitch_marks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["best_pitch_marks"]
        freq_chunks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["freq_chunks"]


        best_pitch_marks = []
        for best_pitch_marks_region in best_pitch_marks_info:
            for best_pitch_marks_freq_chunk in best_pitch_marks_region:
                for i in best_pitch_marks_freq_chunk:
                    best_pitch_marks.append(i)

        new_x = psola.freq_shift_using_td_psola_helper_new_two(x,best_pitch_marks,0.85)
        new_sndarray = []
        for i in range(0,len(new_x)):
            new_sndarray.append(numpy.int16(new_x[i]))

        new_sndarray = voi.make_two_channels(new_sndarray)
        voi.write_to_new_file(filenameFreqShift,numpy.asarray(new_sndarray))

        s = Server().boot()
        s.start()
        dur = sndinfo(filenameFreqShift)[1]
        sf = SfPlayer(filenameFreqShift, speed=1, loop=False)
        t2 = NewTable(length=dur)
        out = Tone(sf, 8000,mul=2).out()
        rec2 = TableRec(out, table=t2)
        rec2.play()
        s.start()
        time.sleep(dur*4)
        s.stop()

        savefileFromTable(t2,filenameSad,0,0)


if __name__ == "__main__":
    filename= "Vocie-samples/salli.wav"
    emotiveSpeech(filename,"Happy")






