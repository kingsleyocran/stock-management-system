import styles from "../page.module.css";

export function Loading() {
  return (
    <div className={`${styles.ldsRoller} ${styles.center}`}>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  );
}

export function CardLoader() {
  return (
    <div className={styles.wrapperContainer}>
      <div className={styles.wrapperCard}>
        <div className={styles.wrapper}>
          <div className={styles.cardLoader}></div>
        </div>

        <div className={styles.wrapper}>
          <div className={styles.cardLoader}></div>
        </div>
        <div className={styles.wrapper}>
          <div className={styles.cardLoader}></div>
        </div>
      </div>

      <div className={styles.wrapperCard}>
        <div className={styles.wrapper}>
          <div className={styles.cardLoader}></div>
        </div>
        <div className={styles.wrapper}>
          <div className={styles.cardLoader}></div>
        </div>
        <div className={styles.wrapper}>
          <div className={styles.cardLoader}></div>
        </div>
      </div>
    </div>
  );
}
