from transmission import *
# These are the functions involve with the algorithm


def function():
    print("this is an algorithm function")
    return 0


# modify table
def update_channel_table(env, table, time_div):
    for ch in range(1, NUM_CH_DEFAULT):
        if get_ch_state(env, ch) == FREE:
            table[ch][time_div] = table[ch][time_div] + 2
        elif get_ch_state(env, ch) == LEASE:
            table[ch][time_div] = table[ch][time_div] + 1
        else:
            pass
    return 1


def select_channel(env, table, time_div):
    ch = 1
    for c in range(1, NUM_CH_DEFAULT):
        if get_ch_state(env, ch) == FREE and (table[ch][time_div] < table[c][time_div]):
            ch = c

    return ch
