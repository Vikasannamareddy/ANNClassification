import h5py
import json
import shutil

MODEL_PATH = 'model.h5'
BACKUP_PATH = 'model.h5.bak'

def remove_keys(obj, keys_to_remove):
    if isinstance(obj, dict):
        for k in list(obj.keys()):
            if k in keys_to_remove:
                del obj[k]
            else:
                remove_keys(obj[k], keys_to_remove)
    elif isinstance(obj, list):
        for item in obj:
            remove_keys(item, keys_to_remove)


def patch_model_h5(path):
    # Backup
    shutil.copy2(path, BACKUP_PATH)
    print(f'Backup created at {BACKUP_PATH}')

    with h5py.File(path, 'r+') as f:
        # model_config is usually stored as an attribute or dataset
        config_json = None
        if 'model_config' in f.attrs:
            raw = f.attrs['model_config']
            if isinstance(raw, bytes):
                config_json = raw.decode('utf-8')
            else:
                config_json = str(raw)
        elif 'model_config' in f:
            raw = f['model_config'][()]
            if isinstance(raw, bytes):
                config_json = raw.decode('utf-8')
            else:
                config_json = str(raw)
        else:
            # Try common Keras attribute
            for k,v in f.attrs.items():
                if k == 'model_config':
                    raw = v
                    config_json = raw.decode('utf-8') if isinstance(raw, bytes) else str(raw)
                    break

        if not config_json:
            print('No model_config found in HDF5 file.')
            return False

        config = json.loads(config_json)

        # Remove problematic keys used in older Keras models
        keys_to_remove = ['batch_shape', 'optional', 'batch_input_shape', 'quantization_config']
        remove_keys(config, keys_to_remove)

        new_config_json = json.dumps(config)

        # Write back
        try:
            if 'model_config' in f.attrs:
                f.attrs['model_config'] = new_config_json
            elif 'model_config' in f:
                del f['model_config']
                f.create_dataset('model_config', data=new_config_json)
            else:
                f.attrs['model_config'] = new_config_json
            print('Patched model_config written to HDF5 file.')
            return True
        except Exception as e:
            print('Failed to write patched config:', e)
            return False

if __name__ == '__main__':
    success = patch_model_h5(MODEL_PATH)
    if success:
        print('Patch completed. You can now try loading the model.')
    else:
        print('Patch failed. Check the file and try manually.')
