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
    
    
    def testRun(self, ctx, workspace_name):
        returnVal = ''
        
        fastaFileIn = '/tmp/muscle/in.fasta'
        fastaFileOut = '/tmp/muscle/out.fasta'
        ff = open( fastaFileIn,'w')
        ff.write('>1\nMTTPVDAPKWPRQIPYIIASEACERFSFYG\n')
        ff.write('>2\nMTTPVDAPAAAAAKWPRQIPYIIASEACERFSFYG\n')
        ff.write('>3\nMTTPVDAPKWPRQIPYIQQQQQQQIASEACERFSFYG\n')
        ff.close()
        
        os.system('/kb/runtime/bin/muscle ' + ' -in ' + fastaFileIn + ' -out ' + fastaFileOut)
        
        with open(fastaFileOut, 'r') as fr:
            returnVal = fr.read()
        return returnVal
    
    def buildGenome2Features(self, ws, workspace_name, featureset_id):
        genome2Features = {}
        featureSet = ws.get_objects([{'ref':workspace_name+'/'+featureset_id}])[0]['data']
        features = featureSet['elements']
        for fId in features:
            genomeRef = features[fId][0]
            if genomeRef not in genome2Features:
                genome2Features[genomeRef] = []
            genome2Features[genomeRef].append(fId)
        return genome2Features
    
    
    
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
        
        fileFastaName = '/tmp/muscle/in.fasta'
        fileOutputName = '/tmp/muscle/out.fasta'
 
        # create workspace client
        token = ctx['token']
        ws = workspaceService(self.workspaceURL, token=token)
                 
        # Build genome2Features hash
        genome2Features = self.buildGenome2Features(ws, workspace_name, featureset_id)
                     
        # Process each genome one by one
        with open(fileFastaName, 'w') as ff:
            for genomeRef in genome2Features:
                 genome = ws.get_objects([{'ref':genomeRef}])[0]['data']
                 featureIds = genome2Features[genomeRef]
                 for feature in genome['features']:
                     for fId in featureIds:
                         if fId == feature['id']:
                             ff.write('>' + fId + '\n' + feature['protein_translation'] + '\n')

        os.system('/kb/runtime/bin/muscle ' + ' -in ' + fileFastaName + ' -out ' + fileOutputName)
        
        with open(fileOutputName, 'r') as fr:
            returnVal = fr.read()
        
#        statinfo = os.stat('/kb/runtime/muscle/muscle3.8.31_i86linux64')
#        returnVal = str(statinfo.st_size)

        #END build_msa

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method build_msa return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]
