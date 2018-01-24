from vega_datasets import data

def test_metadata():
    all_datasets = data.list_datasets()
    local_datasets = data.list_local_datasets()
    for name in all_datasets:
        dataobj = getattr(data, name.replace('-', '_'))

        # Local datasets should all have a description defined
        if name in local_datasets:
            assert len(dataobj.description) > 0

        # Descriptions should either be defined, or be None
        assert dataobj.description is None or len(dataobj.description) > 0

        # References should either be a list, or be None
        assert dataobj.references is None or type(dataobj.references) is list
