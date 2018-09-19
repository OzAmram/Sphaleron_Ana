
from optparse import OptionParser
from NanoReader import *
if __name__ == "__main__":
    
    parser = OptionParser()

    parser.add_option('-i', '--inputfile', metavar='F', type='string', action='store',
                    default   =   'test.root',
                    dest      =   'inputfile',
                    help      =   'input dataset')

    parser.add_option('-o', '--outputfile', metavar='F', type='string', action='store',
                    default   =   'out.root',
                    dest      =   'outputfile',
                    help      =   'input dataset')

    parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                    default   =   'data',
                    dest      =   'set',
                    help      =   'dataset (ie data,ttbar etc)')

    parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                    default   =   'off',
                    dest      =   'grid',
                    help      =   'running on grid off or on')
    parser.add_option('-m', '--modulesuffix', metavar='F', type='string', action='store',
                    default   =   'none',
                    dest      =   'modulesuffix',
                    help      =   'ex. PtSmearUp')
    parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                    default   =   'all',
                    dest      =   'num',
                    help      =   'job number')
    parser.add_option('-j', '--jobs', metavar='F', type='int', action='store',
                    default   =   1,
                    dest      =   'jobs',
                    help      =   'number of jobs')
    parser.add_option('-S', '--split', metavar='F', type='string', action='store',
                    default   =   'file',
                    dest      =   'split',
                    help      =   'split by event of file') #EVENT SPLITTING DOESN'T CURRENTLY WORK

    (options, args) = parser.parse_args()

    NanoReader(inputFile = options.inputfile, outputFile = options.outputfile, nJobs = options.jobs, jobNum = options.num)
