#!/usr/bin/python
# -*- coding: ascii -*-

'''
Created on 06-Aug-2010

@author: Ashish Sharma <ashish424242@gmail.com>
@version: 0.1

***** BEGIN LICENSE BLOCK *****
Version: MPL 1.1

The contents of this file are subject to the Mozilla Public License Version 
1.1 (the "License"); you may not use this file except in compliance with 
the License. You may obtain a copy of the License at 
http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
for the specific language governing rights and limitations under the
License.

The Original Code is Narrator module.

The Initial Developer of the Original Code is
Ashish Sharma <ashish424242@gmail.com>.
Portions created by the Initial Developer are Copyright (C) 2010
the Initial Developer. All Rights Reserved.

***** END LICENSE BLOCK *****
'''

import sys
import os
import time

class Narrator():
    '''Narrator class'''

    def __init__(self):
        '''initialize the narrator'''
        self.path = ''
        self.meta = {}
        pass

    def __next_line(self, fpr):
        '''read a line from script file'''
        row = ' '
        while True:
            row = fpr.readline()
            if row.strip().startswith('#'):
                continue
            break
        return row

    def __read_block(self, fpr):
        '''read the next block of lines'''
        block = []
        line = []
        while True:
            row = self.__next_line(fpr)
            if row == '':
                #FILE END
                return None
            if row.strip() == '--':
                #BLOCK END
                block.append(' '.join(line))
                return block
            elif row == '\n' or row.strip() == '':
                #LINE END
                if len(''.join(line)) > 0:
                    block.append(' '.join(line))
                line = []
            else:    
                line.append(row[:-1])

    def __set_meta(self, fpr):
        '''Set up meta data for current narration'''
        block = self.__read_block(fpr)
        if block is not None:
            self.meta = dict([ (pair[0].strip(), pair[1].strip()) for pair in [ row.split(':') for row in block ]])

        else:
            self.meta = {'TITLE': self.path }

    def __show_text(self, buf):
        '''show text in stylish fashion'''
        for ch in buf:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(0.045)

    def __next_narration(self, fpr):
        '''narrate next part of script'''
        blk = self.__read_block(fpr)
        if blk is None:
            return False
        #Narrate
        self.__show_text('\n'.join(blk))
        return True

    def _welcome(self):
        '''welcome message'''
        msg = ''
        if 'TITLE' in self.meta:
            msg = self.meta['TITLE'] + '\n====>>\n'
        if 'GREETMSG' in self.meta:
            msg += self.meta['GREETMSG'] + '\n'
        if 'BY' in self.meta:
            msg += ('Video presented by ' + self.meta['BY'] + '\n')
        if msg == '':
            msg = 'Let\'s rock.\n'
        msg += 'Start video narration--\n'
        self.__show_text(msg)
    
    def _bye(self):
        '''end message'''
        msg = ''
        if 'ENDMSG' in self.meta:
            msg = self.meta['ENDMSG'] + '\n'
        if 'BY' in self.meta:
            msg += ('Video presented by ' + self.meta['BY'] + '\n')
        if 'EMAIL' in self.meta:
            msg += ('Contact the author at ' + self.meta['EMAIL'] + '\n')
        msg += 'Thanks for watching\n'
        self.__show_text(msg)
    
    def check_script(self, path):
        '''check presence and format of script'''
        #Check if script file exists
        if os.path.isfile(path):
            pass
        else:
            return False
        self.path = path
        return True

    def main_loop(self):
        '''loop and narrate script until it ends'''
        fpr = open(self.path, 'r') 
        self.__set_meta(fpr)
        self._welcome()
        
        loop = True
        while loop:
            inp = raw_input()
            if inp == 'q':
                loop = False
                continue
            if not self.__next_narration(fpr):
                loop = False

        fpr.close()
        self._bye()

def check_args():
    '''check arguments supplied to program
    Return True to continue execution
    and False to stop and exit'''
    if len(sys.argv) != 2:
        print '[-------Usage-------]\n./narrator.py script_to_narrate'
        return False
    else:
        return True

def main():
    '''Entrance point for Program'''
    if check_args():   
        nrt = Narrator()
        if nrt.check_script(sys.argv[1]):
            print 'Narrating with Narrator 0.1\n'
            nrt.main_loop()
        else:
            print 'Error: Bad script file'
    else:
        pass

if __name__ == "__main__":
    main()

