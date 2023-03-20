import mido

# midiin.openVirtualPort()

# def print_message(midi):
#     if midi.isNoteOn():
#         print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
#     elif midi.isNoteOff():
#         print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
#     elif midi.isController():
#         print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())


# port_name = 1

# ports = range(midiin.getPortCount())
# if ports:
#     for i in ports:
#         print(midiin.getPortName(i))
#     print(f"Opening port {port_name}!") 
#     #midiin.openVirtualPort("Virtual Raw MIDI")
#     midiin.openPort(port_name)
#     while True:
#         m = midiin.getMessage(250) # some timeout in ms
#         if m:
#             print_message(m)
# else:
#     print('NO MIDI INPUT PORTS!')



def opem_midi(port):
    with mido.open_input() as inport:
        for msg in inport:
            if msg.note == 50 and msg.type == 'note_on':
                print('beat')
                

opem_midi()