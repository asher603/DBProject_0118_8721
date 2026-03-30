<div align="center" dir="rtl">
  <h1> שלב ב' - שאילתות ואילוצים</h1>
  <p><i>מערכת ניהול בתי חולים (PostgreSQL) - שלב תשאול, אילוצים וניהול עסקאות (Transactions).</i></p>
</div>

---

<div dir="rtl">

##  תוכן עניינים
1. [שאילתות כפולות (SELECT שתי צורות)](#1-שאילתות-כפולות-)
2. [שאילתות SELECT נוספות (מתקדמות)](#2-שאילתות-select-נוספות-)
3. [אילוצים מוגדרים (Constraints)](#3-אילוצים-מוגדרים-)
4. [שאילתות עדכון ומחיקה (UPDATE ו- DELETE)](#4-שאילתות-עדכון-ומחיקה-)
5. [עסקאות בסיס נתונים (COMMIT ו- ROLLBACK)](#5-עסקאות-בסיס-נתונים-)

---

## 1. שאילתות כפולות 
בחלק זה מוצגות 4 שאילתות מורכבות אשר נכתבו ב-2 צורות שונות (בסך הכל 8 שאילתות), לצורך ניתוח הבדלי יעילות.

###  שאילתא 1: מטופלים שביקרו במהלך 2024
**תיאור השאילתא:** שליפת מספרי טלפון ושמות המטופלים שביצעו ביקור (Visit) אצל רופא במהלך שנת 2024 לפחות פעם אחת (מסך מיועד: דשבורד קבלה ומעקב למזכירות).  
**הסבר על ההבדל בין הצורות ויעילות:**
ביצוע השאילתא בעזרת EXISTS לרוב מהיר ויעיל יותר משימוש בצורת ה- IN. הסיבה לעדיפות היא שמנוע מסד הנתונים משתמש בלוגיקת "Short-Circuit" כשהוא משתמש ב-EXISTS. המשמעות היא שברגע שהוא סורק את טבלת ה-VISITS ומוצא את המטופל פעם אחת בלבד בשנת 2024, הוא מחזיר אמת ועוצר מיד! לעומת זאת, שימוש ב- IN יחייב את הפקודה הפנימית לרוץ על כל היסטוריית הביקורים, לאסוף רשימה מלאה בזיכרון, ורק אז לסנן מתוכה עם מנוע ה-IN.

**קוד השאילתא בשיטה עם IN**

 ```sql
SELECT Patient_ID, First_Name, Last_Name, Phone_Number 
FROM PATIENTS 
WHERE Patient_ID IN (
    SELECT Patient_ID 
    FROM VISITS 
    WHERE EXTRACT(YEAR FROM Visit_Date) = 2024
);
```

**קוד השאילתא בשיטה עם EXISTS**

 ```sql
SELECT Patient_ID, First_Name, Last_Name, Phone_Number 
FROM PATIENTS p
WHERE EXISTS (
    SELECT 1 
    FROM VISITS v 
    WHERE v.Patient_ID = p.Patient_ID 
      AND EXTRACT(YEAR FROM v.Visit_Date) = 2024
);
```
Stage_B\images
*צילום הרצה ותוצאות:*
<br><img src="./images/Quary_1.png" width="700">



### ‍ שאילתא 2: עומס בצוות - יותר מ-5 פגישות במאי
**תיאור השאילתא:** מציאת אנשי צוות שצברו עומס ונקבעו להם יותר מ-5 פגישות/תורים עתידיים במהלך חודש מאי (מסך מיועד: לוח עומסים למנהל מחלקה).  
**הסבר על ההבדל בין הצורות ויעילות:**
הדרך האידיאלית להשגת התוצאה היא שימוש ישיר ב- GROUP BY וחיתוך עם HAVING. בקוד המקביל בחרנו לכתוב קריאת "Inline View" (תת-שאילתא בתוך פקודת ה-FROM). קריאה זו מכריחה את השרת לייצר טבלה זמנית פיזית בזיכרון שעליה רק מתבצע החיתוך, תהליך שצורך יותר משאבים באופן משמעותי יחסית פשוט לפילטור ישיר של מנוע האופטימיזציה בעזרת ה-HAVING.

**קוד השאילתא בשיטה עם GROUP BY ו HAVING**

 ```sql
SELECT s.Employee_ID, s.First_Name, s.Last_Name, COUNT(a.Appointment_ID) AS Total_Appointments
FROM STAFF s
JOIN APPOINTMENTS a ON s.Employee_ID = a.Employee_ID
WHERE EXTRACT(MONTH FROM a.Appointment_Date) = 5
GROUP BY s.Employee_ID, s.First_Name, s.Last_Name
HAVING COUNT(a.Appointment_ID) > 5
ORDER BY Total_Appointments DESC;
```

**קוד השאילתא בשיטה עם Inline View**

 ```sql
SELECT Employee_ID, First_Name, Last_Name, Total_Appointments
FROM (
    SELECT Employee_ID, COUNT(Appointment_ID) AS Total_Appointments
    FROM APPOINTMENTS
    WHERE EXTRACT(MONTH FROM Appointment_Date) = 5
    GROUP BY Employee_ID
) AS app_counts
JOIN STAFF s USING (Employee_ID)
WHERE app_counts.Total_Appointments > 5
ORDER BY Total_Appointments DESC;
```

*צילום הרצה ותוצאות:*
<br><img src="./images/Quary_2.png" width="700">


###  שאילתא 3: מציאת חדרים ריקים ללא מיטות
**תיאור השאילתא:** שליפת מספרי חדרים מתוך טבלת החדרים אליהם לא שויכה אף מיטה, כלומר חדרים ריקים לצורך מחסן או שיפוץ (מסך מיועד: מערך תפעול לאבות הבית).  
**הסבר על ההבדל בין הצורות ויעילות:**
למציאת היעדר קשר (צדדים ריקים), LEFT JOIN עובד מצוין שכן הוא יודע לרתום אינדקסים קיימים למנוע הסריקה. זאת לעומת שימוש בפקודת NOT IN שנחשבת רגישה במיוחד לפערים בנתונים - מספיק שבשאילתה הפנימית הוחזרה תוצאה יחידה של NULL, כל ההשוואה של ה-NOT IN קורסת ומחזירה לנו ריק (בגלל לוגיקה משולשת של SQL), ומחייבת סריקת טבלה מלאה (Full Table Scan) שפוגעת אנושות בביצועים.

**קוד השאילתא בשיטה עם NOT IN**

 ```sql
SELECT Room_ID, Room_Number, Room_Type
FROM ROOMS
WHERE Room_ID NOT IN (
    SELECT Room_ID 
    FROM BEDS 
    WHERE Room_ID IS NOT NULL
);
```

**קוד השאילתא בשיטה עם LEFT JOIN ו IS NULL**

 ```sql
SELECT r.Room_ID, r.Room_Number, r.Room_Type
FROM ROOMS r
LEFT JOIN BEDS b ON r.Room_ID = b.Room_ID
WHERE b.Bed_ID IS NULL;
```

*צילום הרצה ותוצאות:*
<br><img src="./images/Quary_3.png" width="700">


###  שאילתא 4: כמות האשפוזים לפי מחלקה בשנת 2024
**תיאור השאילתא:** מקשרת בין מחלקות, חדרים, מיטות ואשפוזים, על מנת לספור ולזהות איזו מחלקה טיפלה בהכי הרבה אשפוזי פנים במהלך 2024. (מסך מיועד: דשבורד מנכ"ל תפוסות בבית החולים).  
**הסבר על ההבדל בין הצורות ויעילות:**
שימוש בשרשרת JOIN מסורתית הוכח כיעיל ביותר. ה-JOIN מבצע הצלבת נתונים בזיכרון בצורה חד-פעמית. למולו, הצורה השנייה נבנתה באמצעות הנחת השאילתא הפנימית בתוך עמודת ה- SELECT (שיטה הנקראת Correlated Subquery). שיטה זו מייצרת את בעיית ה- N+1 הידועה: לשם גישה לשם המחלקה, מנוע המסד מוכרח לרוץ ולהפעיל את תת-השאילתא *שוב ושוב פעם אחת לכל שורת פלט* שקיימת, דבר המעמיס על המסד בצורה בלתי פרופורציונלית.

**קוד השאילתא בשיטה עם Correlated Subquery**

 ```sql
SELECT 
    (SELECT Department_Name FROM DEPARTMENTS d WHERE d.Department_ID = r.Department_ID) AS Dept_Name,
    COUNT(ia.Admission_ID) AS Total_Admissions
FROM INPATIENT_ADMISSIONS ia
JOIN BEDS b ON ia.Bed_ID = b.Bed_ID
JOIN ROOMS r ON b.Room_ID = r.Room_ID
WHERE EXTRACT(YEAR FROM ia.Admission_Date) = 2024
GROUP BY r.Department_ID
ORDER BY Total_Admissions DESC;
```

**קוד השאילתא בשיטה עם chained JOINs**

 ```sql
SELECT 
    d.Department_Name,
    COUNT(ia.Admission_ID) AS Total_Admissions
FROM INPATIENT_ADMISSIONS ia
JOIN BEDS b ON ia.Bed_ID = b.Bed_ID
JOIN ROOMS r ON b.Room_ID = r.Room_ID
JOIN DEPARTMENTS d ON r.Department_ID = d.Department_ID
WHERE EXTRACT(YEAR FROM ia.Admission_Date) = 2024
GROUP BY d.Department_Name
ORDER BY Total_Admissions DESC;
```

*צילום הרצה ותוצאות:*
<br><img src="./images/Quary_4.png" width="700">


---

## 2. שאילתות SELECT נוספות 

*  **שאילתא 5 (אזהרות חייבים על סכומים חריגים):**
  מזהה את מערך המטופלים שצברו בחשבוניות תשלום חובות או חיובים כללים מצטברים שערכם גבוה מ-1500 (שילוב כלי ה-SUM).

  **קוד השאילתא**

   ```sql
  SELECT 
    p.First_Name, p.Last_Name, p.Phone_Number, 
    SUM(i.Total_Amount) as Total_Billed,
    COUNT(i.Invoice_ID) as Invoice_Count
  FROM PATIENTS p
  JOIN INVOICES i ON p.Patient_ID = i.Patient_ID
  GROUP BY p.Patient_ID, p.First_Name, p.Last_Name, p.Phone_Number
  HAVING SUM(i.Total_Amount) > 1500
  ORDER BY Total_Billed DESC;
  ```

  <br><img src="./images/Quary_5.png" width="700">

*  **שאילתא 6 (תרופות שחולקו לרבעון 1):**
  הצגת כמות מרשמים שחולקה מכל תרופה במהלך הרבעון הראשון בלבד, חלוקה ופילוח לשמות החודשים הטקסטואליים באמצעות הפונקציה TO_CHAR.

  **קוד השאילתא**

   ```sql
  SELECT 
    m.Medication_Name, 
    TO_CHAR(v.Visit_Date, 'Month') AS Visit_Month,
    COUNT(pr.Prescription_ID) AS Prescriptions_Count
  FROM MEDICATIONS m
  JOIN PRESCRIPTIONS pr ON m.Medication_ID = pr.Medication_ID
  JOIN VISITS v ON pr.Visit_ID = v.Visit_ID
  WHERE EXTRACT(MONTH FROM v.Visit_Date) BETWEEN 1 AND 3
  GROUP BY m.Medication_Name, TO_CHAR(v.Visit_Date, 'Month')
  ORDER BY Prescriptions_Count DESC;
  ```

  <br><img src="./images/Quary_6.png" width="700">

*  **שאילתא 7 (צוות שמטפל בקהילה ללא תשלום):**
  שליפת כלל אנשי הצוות הרפואי שטיפל במטופלים "מזדמנים" – מטופלים שאינם קיימים כלל במערכת החשבוניות, מה שמעיד על עבודת התנדבות או מקרי חירום מזדמנים.

  **קוד השאילתא**

   ```sql
  SELECT s.First_Name, s.Last_Name, s.Role, COUNT(DISTINCT v.Patient_ID) as Unique_Patients_Handled
  FROM STAFF s
  JOIN VISITS v ON s.Employee_ID = v.Employee_ID
  WHERE v.Patient_ID NOT IN (
      SELECT Patient_ID FROM INVOICES
  )
  GROUP BY s.Employee_ID, s.First_Name, s.Last_Name, s.Role
  ORDER BY Unique_Patients_Handled DESC;
  ```

  <br><img src="./images/Quary_7.png" width="700">

*  **שאילתא 8 (דוח אורך ימי אשפוז חודשי):**
  חישוב מתמטי ותאריכי בין יום שחרור לימי קבלה (Discharge_Date - Admission_Date), המפיק את ממוצע ימי האשפוז מנורמל ומחולק לפי קבוצות קלנדריות של חודש ושנה.
  
  **קוד השאילתא**
  
  ```sql
  SELECT 
    EXTRACT(YEAR FROM Admission_Date) AS Year,
    EXTRACT(MONTH FROM Admission_Date) AS Month,
    COUNT(Admission_ID) AS Total_Admissions,
    ROUND(AVG(Discharge_Date - Admission_Date), 2) AS Avg_Stay_Days
  FROM INPATIENT_ADMISSIONS
  GROUP BY EXTRACT(YEAR FROM Admission_Date), EXTRACT(MONTH FROM Admission_Date)
  ORDER BY Year DESC, Month DESC;
  ```

  <br><img src="./images/Quary_8.png" width="700">

---

## 3. אילוצים מוגדרים (Constraints) 
בוצעה הוספה של אילוצים על מסד הנתונים כדי להקשיח את נכונות הנתונים. מטה מוצגים צילומי השגיאות בעת ניסיון החדרה המנוגד לאילוץ (הפרת אילוץ).

### 1.  אילוץ תקינות טלפון ייחודי (UNIQUE)
מניעת מצב עתידי בו מטופל שמר טלפון שכבר שייך במערכת (טעות הקלדה או זהות בדויה). אל האילוץ unique_phone נשלח ניסיון הכנסת לקוח עם טלפון שקיים, וההפרה יצרה את שגיאת ה-Key הכפול כמוצג.
<br><img src="./images/Constraint_1_Error.png" width="600">

### 2.  אילוץ מינימום אורכים לטלפון (CHECK)
הוספת חוק בסיס עם בדיקת LENGTH(). המספר חייב להכיל לפחות 9 תווים. ניסיון החדרה של המספר "123" עורר את שגיאת ה-Check Constraint כפי שניתן לראות.
<br><img src="./images/Constraint_2_Error.png" width="600">

### 3.  אילוץ תאריכי הגיוני למרפאה (CHECK)
הוספת חוק מניעת הרשמת פגישות ששנתן ישנה יותר משנת 2000. ניסיון החדרה מכוון של מערך משנת 1995 נבלם אוטומטית.
<br><img src="./images/Constraint_3_Error.png" width="600">

---

## 4. שאילתות עדכון ומחיקה 
שאילתות לוגיות של התנהלות בית הספר ופעולות יומיות.

###  עדכוני UPDATE מחלקתיים:

**עדכון 1 - חדרי מחלקת החירום הופכים לטיפול נמרץ:**
* שאילתה שמאתרת קוד מחלקה של "Emergency" ומשדרגת את חדריה ל- Intensive_Care_Unit.
<br><b>מסד נתונים לפי העדכון (Before):</b>
<br><img src="./images/Update_1_before.png" width="600">
<br><b>מסד נתונים לאחר העדכון (After):</b>
<br><img src="./images/Update_1_after.png" width="600">

**עדכון 2 - קנס בעיות זיהוי בחשבון:**
* הגדלת החוב ב-10% עבור חשבוניות שמקושרות למטופל בעל טלפון חסר/בלתי-תקין.
<br><b>מסד נתונים לפי העדכון (Before):</b>
<br><img src="./images/Update_2_before.png" width="600">
<br><b>מסד נתונים לאחר העדכון (After):</b>
<br><img src="./images/Update_2_after.png" width="600">

**עדכון 3 - ארכוב כתובות ישנות:**
* עדכון כתובת לארכיון לכל המטופלים שאין להם ביקורים רשומים משנת 2020.
<br><b>מסד נתונים לפי העדכון (Before):</b>
<br><img src="./images/Update_3_before.png" width="600">
<br><b>מסד נתונים לאחר העדכון (After):</b>
<br><img src="./images/Update_3_after.png" width="600">

---

###  מחיקות DELETE ארגוניות:

**מחיקה 1 - ביטול תורים (Appointments) למחלקה מבוטלת:**
* מחיקת התורים העתידיים ששייכים לאנשי צוות תחת מחלקה שנסגרה.
 **היגיון עסקי:** מניעת הגעת מטופלים למחלקה לא פעילה וייעול מערכת זימון התורים.
<br><b>מסד נתונים לפני המחיקה (Before):</b>
<br><img src="./images/Delete_1_before.png" width="600">
<br><b>מסד נתונים לאחר המחיקה (After):</b>
<br><img src="./images/Delete_1_after.png" width="600">

**מחיקה 2 - גריטת מיטות במחסנים:**
* מנתקים ומוחקים כליל רשומות של מיטות ממרפאות/חדרים שעוברים לידי מערך התחזוקה (Maintenance).
 **היגיון עסקי:** עדכון מצבת המלאי בבית החולים לקראת שיפוץ חדרים, למניעת שיבוץ אשפוז שגוי בחדר בשיפוץ.
<br><b>מסד נתונים לפני המחיקה (Before):</b>
<br><img src="./images/Delete_2_before.png" width="600">
<br><b>מסד נתונים לאחר המחיקה (After):</b>
<br><img src="./images/Delete_2_after.png" width="600">

**מחיקה 3 - מחיקת חשבוניות ישנות של מטופלים צעירים:**
* שאילתה לא-טריוויאלית המוחקת חשבוניות ישנות (לפני 2023) עבור מטופלים שנולדו משנת 2008 ומעלה (קטינים). השאילתה מקשרת בין טבלת החשבוניות (INVOICES) לטבלת המטופלים (PATIENTS).
 **היגיון עסקי:** ניקוי חובות היסטוריים שסובסדו מזמן על ידי המדינה/קופות החולים, כדי להוריד עומס ממערכת הגבייה הפעילה.
<br><b>מסד נתונים לפני המחיקה (Before):</b>
<br><img src="./images/Delete_3_before.png" width="600">
<br><b>מסד נתונים לאחר המחיקה (After):</b>
<br><img src="./images/Delete_3_after.png" width="600">


---

## 5. עסקאות בסיס נתונים (COMMIT / ROLLBACK) 

### נסיון 1: פעולת ROLLBACK בתוך טרנזקציה פתוחה
הפעלנו בלוק עבודה בעזרת הטרנזקציה BEGIN. ביצענו פקודת UPDATE שהפכה חדר תפעולי למצב "VIP_Temporary". במרכז הטרנזקציה שלפנו את המידע לזיכרון וראינו שהשינויים בוצעו במלואם. בשלב השלישי הוטמעה בבקיאות הפקודה הפוסלת ROLLBACK שהדגימה שחזרנו בצורה מסוללת למצב המדויק מן ההתחלה, והמידע לא נשמר לדיסק.

<br><b>שלב א' - מצב בסיס הנתונים בתחילת הדרך:</b>
<br><img src="./images/rollback_start.png" width="600">
<br><b>שלב ב' - מצב בסיס הנתונים תוך כדי הטרנזקציה (חדר מס' 1 התעדכן):</b>
<br><img src="./images/rollback_mid.png" width="600">
<br><b>שלב ג' - מצב בסיס הנתונים אחרי פקודת ביטול ROLLBACK:</b>
<br><img src="./images/rollback_end.png" width="600">

---

### נסיון 2: פעולת COMMIT בתוך טרנזקציה פתוחה
בדוגמא כזו יצרנו עדכון סיומת לשם התרופה (הוספת סטרינג "Updated"), והפעם קיבענו למסד הנתונים כדי להוריד לדיסק לצמיתות בעזרת COMMIT. לאחר השמירה הוכחה השמירה הוודאית.

<br><b>שלב א' - מצב ההתחלתי של שם התרופה:</b>
<br><img src="./images/commit_start.png" width="600">
<br><b>שלב ב' - מצב הנתונים בתוך הבלוק העצמאי (שם התרופה השתנה):</b>
<br><img src="./images/commit_mid.png" width="600">
<br><b>שלב ג' - מצב הנתונים הסופי והמתועד, לאחר חתימת השמירה:</b>
<br><img src="./images/commit_end.png" width="600">

</div>
