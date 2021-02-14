from transmission import *
# These are the functions involve with the algorithm


def function():
    print("this is an algorithm function")
    return 0


# modify table
def update_channel_table(env, table, time_div):
    c = 1
    while c < NUM_CH_DEFAULT:
        if get_ch_state(env, c) == FREE:
            table[c][time_div] += 3
        elif get_ch_state(env, c) == LEASE:
            table[c][time_div] = table[c][time_div] + 2
        else:
            table[c][time_div] = table[c][time_div] + 1
        c += 1
        # print(table)
    return 1


def select_channel(env, table, time_div):
    ch = 0
    c = 1
    while c < NUM_CH_DEFAULT:
        if get_ch_state(env, c) == FREE and (table[ch][time_div] < table[c][time_div]):
            ch = c
        c += 1

    return ch
