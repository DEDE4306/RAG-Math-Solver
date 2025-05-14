import pandas as pd
import re
import os

class FormulaDataCleaner:
    def __init__(self, input_path, output_path = None):
        self.input_path = input_path
        self.output_path = output_path or self._default_output_path()

    def _default_output_path(self):
        base, ext = os.path.splitext(self.input_path)
        return f"{base}_cleaned{ext}"

    def clean(self):
        df = pd.read_csv(self.input_path)
        df = df[df['label'] == True]
        df.to_csv(self.output_path, index=False)
        print(f"清洗完成，保存至: {self.output_path}")