#BEGIN_HEADER
from biokbase.workspace.client import Workspace as workspaceService
import os
#END_HEADER


class msa_muscle:
    '''
    Module Name:
    msa_muscle

    Module Description:
    A KBase module: msa_muscle
This sample module contains one small method - count_contigs.
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def build_msa(self, ctx, workspace_name, featureset_id, msa_id):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN build_msa
        returnVal = ''
        
        statinfo = os.stat('/kb/runtime/muscle/muscle')
        returnVal = str(statinfo.st_size)
        
        #END build_msa

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method build_msa return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]
