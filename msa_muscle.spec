/*
A KBase module: msa_muscle
This sample module contains one small method - count_contigs.
*/

module msa_muscle {

	/*
	A string representing a FeatureSet reference.
	*/
	typedef string featureset_id;
	
	/*
	A string representing a MSA reference.
	*/
	typedef string msa_id;

	/*
	A string representing a workspace name.
	*/
	typedef string workspace_name;

	funcdef build_msa(workspace_name,featureset_id, msa_id) returns (string ) authentication required;
};