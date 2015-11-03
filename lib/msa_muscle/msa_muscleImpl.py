#BEGIN_HEADER
from biokbase.workspace.client import Workspace as workspaceService
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_protein
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
    fileFastaName = '/tmp/muscle/in.fasta'
    fileOutputName = '/tmp/muscle/out.fasta'
    
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
    
    def exportFasta(self, ws, workspace_name, featureset_id):
        # Build genome2Features hash
        genome2Features = self.buildGenome2Features(ws, workspace_name, featureset_id)
        
        # Process each genome one by one
        records = []
        for genomeRef in genome2Features:
            genome = ws.get_objects([{'ref':genomeRef}])[0]['data']
            featureIds = genome2Features[genomeRef]
            for feature in genome['features']:
                for fId in featureIds:
                    if fId == feature['id']:
                        record = SeqRecord(Seq(feature['protein_translation']), id=fId, description=genomeRef)
                        records.append(record)
        SeqIO.write(records, self.fileFastaName, "fasta")
    
    def createMSA(self, ws, workspace_name, featureset_id, msa_id):
        alignment_length = 0
        msa = {
            'name' : 'multiple alignmemnt for FeatureSet: ' + featureset_id,
            'sequence_type': 'protein',
            'alignment_length': 0,
            'alignment': {},
            'row_order': []
        }
        for record in SeqIO.parse( self.fileOutputName, "fasta"):
            msa['row_order'].append(record.id)
            msa['alignment'][record.id] = record.seq
            alignment_length = len(record.seq)
            msa['alignment_length'] = alignment_length
        
        ws.save_objects({'workspace':workspace_name, 'objects':[{'name':msa_id, 'type':'KBaseTrees.MSA', 'data': msa}]})
        return str(msa)
    
    
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
 
        # create workspace client
        token = ctx['token']
        ws = workspaceService(self.workspaceURL, token=token)
        
        # Export fasta
        self.exportFasta(ws, workspace_name, featureset_id)
        
        # Run muscle
        os.system('/kb/runtime/bin/muscle ' + ' -in ' + self.fileFastaName + ' -out ' + self.fileOutputName)
        
        # Create MSA object
        returnVal = self.createMSA(ws, workspace_name, msa_id)
        

        #END build_msa

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method build_msa return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]
