from src.svd import *
from src.tf_idf import *
from src.utils.visualization import *


def main():
    test_text = """בתחקיר שפורסם בכאן חדשות סיפר א', שנפגש עם אוחובסקי לפני כשנה וחצי, כי השניים קבעו להיפגש לאחר ששוחחו באפליקציית היכרויות. אוחובסקי, כך אמר, השתמש בשם בדוי אך שלח את תמונותיו האמיתיות. "הוא תקשר כמו חיה", סיפר א'. "יותר מחמש פעמים הוא ניסה להפוך אותי בכוח ולגעת". הוא ציין כי ביקש ממנו להפסיק באופן נחרץ, ולפי הפרסום גם עבר בדיקת פוליגרף שבה נמצא דובר אמת."""

    tf = create_tf_table(test_text)
    idf = create_idf_table(test_text)
    svd = create_svd_table(tf, idf)

    print("\n\nSVD TABLE: \n")
    [print(key, value) for key, value in svd.items()]

    print("\n\nIDF TABLE: \n")
    [print(key, ': %.3f' % value) for key, value in idf.items()]

    print("\n\nTF TABLE: \n")
    [print(key, value) for key, value in tf.items()]


if __name__ == "__main__":
    main()
