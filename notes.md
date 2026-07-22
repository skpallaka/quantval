# Backtester — Learning Notes

Personal reference for methods/concepts:

## Pandas

- `.rolling(window).mean()` — sliding window average over the last N rows. Used in MA crossover for fast/slow moving averages.
- `.diff()` — difference between each row and the previous row. today - yesterday.
- `.where(condition, other)` — keeps value where condition is True, replaces with `other` where False.
- `.astype(type)` — converts a Series to a different type (e.g. bool -> int, int -> float).
- `.dropna()` / `.isna()` / `.notna()` — drop / check for missing (NaN) values.

## NumPy

- (add as used)

## General Python

- `from X import Y` — imports only `Y` from module/file `X`. Path matters depends on where the script is *run from*, not where the file lives.
- `if __name__ == "__main__":` — code block that only runs when the file is executed directly, not when it's imported by another file.

## Git

- `git checkout -b <branch>` — create a new branch and switch to it.
- `git add <files>` — stage specific changes to include in the next commit. `git add .` stages everything changed/new.
- `git commit -m "message"` — save staged changes as a permanent snapshot in history.
- `git push -u origin <branch>` — upload the branch to GitHub.
- PR (Pull Request) — opened on GitHub, proposes merging one branch into another (usually into `main`). Review + merge there.
- `git checkout main && git pull` — switch back to main, get the latest merged changes.
- `git log --oneline -N` — see the last N commits, one line each.
- `git status` — see current branch + what's staged/unstaged/untracked.

## Bugs

1. **Import path depends on where you run the script from.** `python3 data/fetch.py` vs `python3 test_ma.py` (from root) changed whether `from cache import ...` could find `cache.py`. Fixed by using absolute imports (`from data.cache import ...`) and adding `__init__.py` files to mark folders as packages.
2. **SQLite path was relative to terminal's current directory, not the script's location.** Caused `unable to open database file` when running from the wrong folder. Fixed with `os.path.dirname(os.path.abspath(__file__))`.
3. **Cache completeness check compared date strings incorrectly around holidays/weekends.** `"2015-01-02" <= "2015-01-01"` was False even though the cache was valid, because trading data doesn't exist for non-trading days. Fixed with a separate `fetch_log` table tracking requested ranges, not inferring from price data itself.
4. **Cache-hit and cache-miss paths returned inconsistent DataFrame schemas** (column casing/order/extra columns differed). Caught by comparing two printouts side by side — fixed by normalizing columns in one place before returning.
5. **`.astype(int)` on a signal silently turned "not enough history yet" (NaN) into "flat" (0)** — misleading, since it looked like a real decision. Fixed with `.astype(float)` + `.where(condition, other=np.nan)` to preserve the distinction.