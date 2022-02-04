# Imports
from typing import Optional
from skimage import io as skimio, util as skimutil
import random
import configparser
from pathlib import Path, PurePath
import shutil
import json
import sys
from numpy import ndarray

# Config the .ini file
config = configparser.ConfigParser()
config.read("NoiseAdder.ini")


def test_seed(s: Optional[str], name: str) -> Optional[int]:
    if s.lower() == "none":
        return None
    else:
        try:
            s = int(s)
        except ValueError:
            print(f"The {name} seed must be a number or None")
            sys.exit()
        return s


def add_list_weighted(weighted_list: list, value: int, name: str) -> list:
    if len(weighted_list) == 0:
        weighted_list.append([value, name])
    else:
        weighted_list.append([weighted_list[-1][0] + value, name])
    return weighted_list


# Local Variables
path1 = config.get("General", "Original_Path")
path2 = config.get("General", "Modified_Path")
suffixes = json.loads(config.get("General", "Suffix"))
overwrite = config.getboolean("Settings", "Overwrite")
targetPercentage = config.getfloat("Settings", "Add_Noise_Rate")
save2 = config.getboolean("Settings", "Save_Unchanged_Image")
advanced = config.getboolean("Advanced Noise Settings", "Activate")
if not advanced:
    style = config.get("Noise Settings", "Noise_Style")
    seed = config.get("Noise Settings", "seed")
    mean = config.getfloat("Noise Settings", "mean")
    var = config.getfloat("Noise Settings", "variance")
    amount = config.getfloat("Noise Settings", "amount")
else:
    dictStyles = {}
    weightedVal = []
    gaussian = config.getboolean("Advanced Noise Settings", "Activate_Gaussian")
    if gaussian:
        weight = config.getfloat("Advanced Noise Settings", "Weight_Gaussian")
        seed = test_seed(config.get("Advanced Noise Settings", "Seed_Gaussian"), "gaussian")
        minM = config.getfloat("Advanced Noise Settings", "Min_Mean_Gaussian")
        maxM = config.getfloat("Advanced Noise Settings", "Max_Mean_Gaussian")
        minV = config.getfloat("Advanced Noise Settings", "Min_Variance_Gaussian")
        maxV = config.getfloat("Advanced Noise Settings", "Max_Variance_Gaussian")
        weightedVal = add_list_weighted(weightedVal, weight, "gaussian")
        dictStyles["gaussian"] = [seed, minM, maxM, minV, maxV]
    poisson = config.getboolean("Advanced Noise Settings", "Activate_Poisson")
    if poisson:
        weight = config.getfloat("Advanced Noise Settings", "Weight_Poisson")
        seed = test_seed(config.get("Advanced Noise Settings", "Seed_Poisson"), "poisson")
        weightedVal = add_list_weighted(weightedVal, weight, "poisson")
        dictStyles["poisson"] = [seed]
    salt = config.getboolean("Advanced Noise Settings", "Activate_Salt")
    if salt:
        weight = config.getfloat("Advanced Noise Settings", "Weight_Salt")
        seed = test_seed(config.get("Advanced Noise Settings", "Seed_Salt"), "salt")
        minA = config.getfloat("Advanced Noise Settings", "Min_Amount_Salt")
        maxA = config.getfloat("Advanced Noise Settings", "Max_Amount_Salt")
        weightedVal = add_list_weighted(weightedVal, weight, "salt")
        dictStyles["salt"] = [seed, minA, maxA]
    pepper = config.getboolean("Advanced Noise Settings", "Activate_Pepper")
    if pepper:
        weight = config.getfloat("Advanced Noise Settings", "Weight_Pepper")
        seed = test_seed(config.get("Advanced Noise Settings", "Seed_Pepper"), "pepper")
        minA = config.getfloat("Advanced Noise Settings", "Min_Amount_Pepper")
        maxA = config.getfloat("Advanced Noise Settings", "Max_Amount_Pepper")
        weightedVal = add_list_weighted(weightedVal, weight, "pepper")
        dictStyles["pepper"] = [seed, minA, maxA]
    sp = config.getboolean("Advanced Noise Settings", "Activate_S&P")
    if sp:
        weight = config.getfloat("Advanced Noise Settings", "Weight_S&P")
        seed = test_seed(config.get("Advanced Noise Settings", "Seed_S&P"), "s&p")
        minA = config.getfloat("Advanced Noise Settings", "Min_Amount_S&P")
        maxA = config.getfloat("Advanced Noise Settings", "Max_Amount_S&P")
        minP = config.getfloat("Advanced Noise Settings", "Min_Proportion_Of_Salt")
        maxP = config.getfloat("Advanced Noise Settings", "Max_Proportion_Of_Salt")
        weightedVal = add_list_weighted(weightedVal, weight, "s&p")
        dictStyles["s&p"] = [seed, minA, maxA, minP, maxP]
    spe = config.getboolean("Advanced Noise Settings", "Activate_Speckle")
    if spe:
        weight = config.getfloat("Advanced Noise Settings", "Weight_Speckle")
        seed = test_seed(config.get("Advanced Noise Settings", "Seed_Speckle"), "speckle")
        minM = config.getfloat("Advanced Noise Settings", "Min_Mean_Speckle")
        maxM = config.getfloat("Advanced Noise Settings", "Max_Mean_Speckle")
        minV = config.getfloat("Advanced Noise Settings", "Min_Variance_Speckle")
        maxV = config.getfloat("Advanced Noise Settings", "Max_Variance_Speckle")
        weightedVal = add_list_weighted(weightedVal, weight, "speckle")
        dictStyles["speckle"] = [seed, minM, maxM, minV, maxV]
    if len(dictStyles) == 0:
        print("You cannot choose to have 0 styles activated")
        sys.exit()


def save_image(p: Path, image: ndarray) -> None:
    while True:
        try:
            if path1 == path2 and not overwrite:
                skimio.imsave(f"{path2}\\{str(p.parent.relative_to(path1))}\\modified_{PurePath(p).name}",
                              skimutil.img_as_ubyte(image))
            else:
                skimio.imsave(f"{path2}\\{str(p.relative_to(path1))}", skimutil.img_as_ubyte(image))
        except FileNotFoundError:
            Path(f"{path2}\\{str(p.relative_to(path1))}").parent.mkdir(parents=True)
            continue
        break


def add_noise_advanced(p: Path) -> None:
    img = skimio.imread(str(p)) / 255.0
    stylenum = weightedVal[-1][0] * random.random()
    i = 0
    while i < len(weightedVal):
        if weightedVal[i][0] >= stylenum:
            break
        i += 1
    adv_style = weightedVal[i][1]
    adv_style_info = dictStyles[weightedVal[i][1]]
    if adv_style == "gaussian" or adv_style == "speckle":
        m = (adv_style_info[2] - adv_style_info[1]) * random.random() + adv_style_info[1]
        v = (adv_style_info[4] - adv_style_info[3]) * random.random() + adv_style_info[3]
        gimg = skimutil.random_noise(img, mode=adv_style, seed=adv_style_info[0], mean=m, var=v)
    elif adv_style == "salt" or adv_style == "pepper":
        a = (adv_style_info[2] - adv_style_info[1]) * random.random() + adv_style_info[1]
        gimg = skimutil.random_noise(img, mode=adv_style, seed=adv_style_info[0], amount=a)
    elif adv_style == "s&p":
        a = (adv_style_info[2] - adv_style_info[1]) * random.random() + adv_style_info[1]
        svp = (adv_style_info[4] - adv_style_info[3]) * random.random() + adv_style_info[3]
        gimg = skimutil.random_noise(img, mode=adv_style, seed=adv_style_info[0], amount=a, salt_vs_pepper=svp)
    else:
        gimg = skimutil.random_noise(img, mode=adv_style, seed=adv_style_info[0])
    save_image(p, gimg)


def add_noise(p: Path) -> None:
    img = skimio.imread(str(p))/255.0
    if style == "gaussian" or style == "speckle":
        gimg = skimutil.random_noise(img, mode=style, seed=seed, mean=mean, var=var)
    elif style in ["salt", "pepper", "s&p"]:
        gimg = skimutil.random_noise(img, mode=style, seed=seed, amount=amount)
    else:
        gimg = skimutil.random_noise(img, mode=style, seed=seed)
    save_image(p, gimg)


def noise_adder() -> None:
    # Create path2 directory if non-existent
    if not Path(path2).is_dir():
        Path(path2).mkdir(parents=True)

    # Test if style and seed are valid
    if not advanced:
        global style, seed, mean, var, amount
        seed = test_seed(seed, "")
        style = style.lower()
        if style not in ["gaussian", "poisson", "salt", "pepper", "s&p", "speckle"]:
            print("The style must be either gaussian, poisson, salt, pepper, s&p or speckle")
            return

    i = 0
    for path in Path(path1).rglob("*"):
        if path.is_file():
            if PurePath(path).suffix.lstrip(".") in suffixes:
                i += 1
    print(f"Found {i} picture files")

    i = 0
    for path in Path(path1).rglob("*"):
        if path.is_file():
            if PurePath(path).suffix.lstrip(".") in suffixes:
                i += 1
                if random.random() <= targetPercentage:
                    if not advanced:
                        add_noise(path)
                    else:
                        add_noise_advanced(path)
                else:
                    if save2 and path1 != path2:
                        while True:
                            try:
                                shutil.copy(path, f"{path2}\\{str(path.relative_to(path1))}")
                            except FileNotFoundError:
                                Path(f"{path2}\\{str(path.relative_to(path1))}").parent.mkdir(parents=True)
                                continue
                            break
                if i % 100 == 0:
                    print(f"Processed {i} picture files")
    print("Finished")


if __name__ == "__main__":
    noise_adder()
