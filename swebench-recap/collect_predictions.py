import os
import json

# -- config area --

# the directory that have all the task result dirs
RESULTS_BASE_DIR = './trajectories/your_dir'

FOLDER_PREFIX = 'no_config__gpt-4.1__t-0.00__p-1.00__c-10.00___'
MODEL_NAME = 'recap-gpt-4.1__t-0.00__p-1.00__c-10.00'

OUTPUT_FILE = 'predictions_recap-gpt-4.1__t-0.00__p-1.00__c-10.00.jsonl'

# -- main logic --

def collect_and_generate_predictions():
    print(f"scanning '{os.path.abspath(RESULTS_BASE_DIR)}'...")
    
    if not os.path.isdir(RESULTS_BASE_DIR):
        print(f"error: cannot find dir '{RESULTS_BASE_DIR}'")
        return

    try:
        output_f = open(OUTPUT_FILE, 'w', encoding='utf-8')
    except IOError as e:
        print(f"error: cannot create or open '{OUTPUT_FILE}'. check for permission, info: {e}")
        return

    found_count = 0
    processed_count = 0
    missing_patch_count = 0

    for folder_name in os.listdir(RESULTS_BASE_DIR):
        if folder_name.startswith(FOLDER_PREFIX) and os.path.isdir(os.path.join(RESULTS_BASE_DIR, folder_name)):
            found_count += 1
            instance_id = folder_name.replace(FOLDER_PREFIX, '', 1)
            
            patch_filename = f"{instance_id}.patch"
            patch_filepath = os.path.join(RESULTS_BASE_DIR, folder_name, instance_id, patch_filename)
            
            prediction_content = ""
            
            if os.path.exists(patch_filepath):
                try:
                    with open(patch_filepath, 'r', encoding='utf-8') as patch_f:
                        prediction_content = patch_f.read()
                    print(f"  [✓] found and read: {patch_filepath}")
                except Exception as e:
                    print(f"  [!] warning: error reading {patch_filepath}, replacing with empty string. error: {e}")
            else:
                missing_patch_count += 1
                print(f"  [✗] no patch file found: {patch_filepath}, replacing with empty string")

            prediction_record = {
                "instance_id": instance_id,
                "model_name_or_path": MODEL_NAME,
                "model_patch": prediction_content
            }
            
            output_f.write(json.dumps(prediction_record) + '\n')
            processed_count += 1

    output_f.close()

    print("\n" + "="*50)
    print("🎉 collection complete")
    print(f"  - {found_count} folders found")
    print(f"  - {processed_count} processed and written")
    print(f"  - of which {missing_patch_count} task does not have .patch file")
    print(f"  - result saved in: {os.path.abspath(OUTPUT_FILE)}")
    print("="*50)


if __name__ == "__main__":
    collect_and_generate_predictions()
