def stop_long(buy, stop_short, rate=1):
    risk = buy - stop_short
    stop_long = buy + risk * rate
    print(f"risk = {risk:.3f}")
    print(f"stop long = {stop_long}")