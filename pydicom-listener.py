from pynetdicom import AE, evt, AllStoragePresentationContexts, debug_logger


# Implement a handler for evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event."""
    # Decode the C-STORE request's Data Set parameter to a pydicom Dataset
    ds = event.dataset

    # Add the File Meta Information``
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename
    print("===>", ds.SOPInstanceUID)
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # Return a 'Success' status
    return 0x0000


handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
ae = AE()

# Support presentation contexts for all storage SOP Classes
ae.supported_contexts = AllStoragePresentationContexts

# Start listening for incoming association requests
ae.start_server(("", 11112), evt_handlers=handlers)
