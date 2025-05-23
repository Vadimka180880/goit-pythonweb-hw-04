import asyncio
import aiofiles
import shutil
import logging
from pathlib import Path
import argparse

logging.basicConfig(level=logging.ERROR, filename='errors.log', 
        filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path: Path, target_folder: Path):
    try:
        ext = file_path.suffix[1:] or "no_extension"  
        new_dir = target_folder / ext
        new_dir.mkdir(parents=True, exist_ok=True) 
        await asyncio.to_thread(shutil.copy2, file_path, new_dir / file_path.name)
    except Exception as e:              
        logging.error(f"Failed to copy {file_path}: {e}")
        
async def read_folder(source: Path, target: Path):
    tasks = []
    async for file in async_scan(source):
        if file.is_file():
            tasks.append(copy_file(file, target))
    await asyncio.gather(*tasks)  

                
async def async_scan(folder: Path):
    for path in folder.rglob("*"):
        yield path
        
def main():
    parser = argparse.ArgumentParser(description="Async file sorter")
    parser.add_argument("source", type=Path, help="Source folder")
    parser.add_argument("output", type=Path, help="Destination folder")  
    args = parser.parse_args()
    if not args.source.exists():    
            print(f"Source folder '{args.source}' does not exist.")
            return
    asyncio.run(read_folder(args.source, args.output))

if __name__ == "__main__":
    main()      