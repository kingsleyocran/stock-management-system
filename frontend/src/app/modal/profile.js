"use client";
import Image from "next/image";
import styles from "../page.module.css";
import modalStyles from "../modal.module.css";
import { useState, useRef } from "react";
import { faCloudUpload, faUserCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Loading } from "./utils";

export function UserProfile({ onShow, userDetails }) {
  const profileElement = useRef();
  const image = useRef(null);
  const [showLoading, setShowLoading] = useState(false);
  const [showError, setShowError] = useState("");
  const [done, setDone] = useState("");
  const [sentProduct, setSentProduct] = useState(false);
  const [email, setEmail] = useState(userDetails?.email);

  const handleClose = (e) => {
    if (sentProduct) {
      onShow();
      windows.location.reload();
    }
    onShow();
  };
  const handleSubmit = (e) => {
    e.preventDefault();
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleChangeProfileImage = (e) => {
    if (e.target.files.length > 0) {
      const imageUploaded = e.target.files[0];
      const src = URL.createObjectURL(imageUploaded);

      profileElement.current.src = src;
      //   profileElement.current.style.display = "block";
      image.current = imageUploaded;
    }
  };

  return (
    <>
      <div className={styles.modal}>
        <div className={styles.modalContent}>
          <span className={styles.close} onClick={handleClose}>
            &times;
          </span>

          {showError.length > 0 ? (
            <p className={styles.errorMsg}>{showError}</p>
          ) : (
            ""
          )}

          {done.length > 0 ? <h1>{done}</h1> : ""}

          <div className={styles.addProductContainer}>
            <div className={modalStyles.formInput}>
              <div className={modalStyles.preview}>
                <Image
                  src={
                    userDetails.profile_pic.length > 0
                      ? userDetails.profile_pic
                      : "./avatar.svg"
                  }
                  alt="user-profile"
                  ref={profileElement}
                  width={180}
                  height={220}
                  className={modalStyles.avatar}
                  codemod={"responsive"}
                />
              </div>
              <label htmlFor="upload-file">
                <FontAwesomeIcon icon={faCloudUpload} /> &nbsp;Update Profile
                Pic
              </label>
              <input
                type="file"
                id="upload-file"
                accept="image/*,.png,.jpg"
                onChange={handleChangeProfileImage}
                disabled={showLoading}
              />
            </div>

            {showLoading ? (
              <div className={`${styles.center} ${styles.done}`}>
                <Loading />
              </div>
            ) : (
              ""
            )}

            <form action="" onSubmit={handleSubmit}>
              <div className={styles.addProductInputDetails}>
                <label htmlFor="first_name">First Name</label>
                <input
                  id="first_name"
                  type="text"
                  name="first_name"
                  disabled
                  value={userDetails.first_name}
                />
                <label htmlFor="last_name">Last Name</label>
                <input
                  id="last_name"
                  type="text"
                  name="last_name"
                  disabled
                  value={userDetails.last_name}
                />

                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  name="email"
                  disabled={showLoading}
                  onChange={handleEmailChange}
                  value={email}
                />

                <button type="submit" disabled={showLoading}>
                  Update Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
