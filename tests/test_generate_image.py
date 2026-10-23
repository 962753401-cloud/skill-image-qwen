import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_image.py"
ORIGINAL = "生成一张简洁的产品展示图"
OPTIMIZED = (
    "生成一张横版产品展示图，主体居中，柔和棚拍光，浅灰背景，"
    "画面干净，预留标题空间，避免文字、水印和杂乱元素。"
)
EXPLANATION = (
    "补充了横版构图、主体位置、棚拍光线、背景色彩和负面约束，"
    "让原始需求成为可直接执行的完整提示词。"
)


class GenerateImageWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = os.environ.copy()
        for name in ("DASHSCOPE_API_KEY", "DASHSCOPE_BASE_URL"):
            self.env.pop(name, None)
        self.env["TEMP"] = self.temp.name
        self.env["TMP"] = self.temp.name

    def tearDown(self):
        self.temp.cleanup()

    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=str(ROOT),
            env=self.env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def optimize(self):
        result = self.run_script(
            "optimize",
            "--original-prompt",
            ORIGINAL,
            "--optimized-prompt",
            OPTIMIZED,
            "--change-explanation",
            EXPLANATION,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.token_after(result.stdout, "Token A")

    @staticmethod
    def token_after(output, label):
        lines = output.splitlines()
        for index, line in enumerate(lines):
            if label in line and index + 1 < len(lines):
                return lines[index + 1].strip()
        raise AssertionError(f"{label} not found in output")

    def test_local_workflow_stops_at_missing_key(self):
        token_a = self.optimize()
        prepared = self.run_script(
            "prepare",
            "--token",
            token_a,
            "--optimized-prompt",
            OPTIMIZED,
        )
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        token_b = self.token_after(prepared.stdout, "Token B")

        generated = self.run_script(
            "generate",
            "--token",
            token_b,
            "--prompt",
            OPTIMIZED,
        )
        self.assertNotEqual(generated.returncode, 0)
        self.assertIn("DASHSCOPE_API_KEY", generated.stderr)

        pending = Path(self.temp.name) / "skill_image_qwen_pending" / f"{token_b}.json"
        self.assertTrue(pending.is_file())

    def test_prepare_rejects_missing_optimize_token(self):
        result = self.run_script(
            "prepare",
            "--token",
            "0" * 64 + "-deadbeef",
            "--optimized-prompt",
            OPTIMIZED,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("必须先完成 optimize", result.stderr)

    def test_prepare_rejects_changed_prompt(self):
        token_a = self.optimize()
        result = self.run_script(
            "prepare",
            "--token",
            token_a,
            "--optimized-prompt",
            OPTIMIZED + " 新增一朵花。",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不一致", result.stderr)

    def test_generate_rejects_missing_prepare_token(self):
        result = self.run_script(
            "generate",
            "--token",
            "0" * 64 + "-deadbeef",
            "--prompt",
            OPTIMIZED,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("必须先完成 prepare", result.stderr)


if __name__ == "__main__":
    unittest.main()
