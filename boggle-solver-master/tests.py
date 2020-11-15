def main():
    boggle()
    NN()
def NN():
    import TrainBoggle
    return TrainBoggle.run()
def boggle():
    import boggle1 
    #main runs a test of the boggle accuracy.
    if 45 == len(boggle1.SolveBoard(['T','W','I','H','P','U','H','E','T','S','J','L','B','V','T','M'])):
        return True
    else:
        return False

if __name__ == '__main__':
    main()