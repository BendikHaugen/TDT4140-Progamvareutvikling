import React from "react";

import { Link } from "react-router-dom";

import { withRouter } from "react-router";

import styles from "./settings.module.css";

import url from "../../consts/django-url"

const Settings = props => {
  const newWorkout = () => {
    props.newWorkout();
    if (!props.creatingNewWorkout) {
      props.history.push("/");
    }
  };

  const newExercise = () => {
    props.newExercise();
    if (!props.creatingNewExercise) {
      props.history.push("/");
    }
  };

  const hideExercises = () => {
    props.hideExercises();
    props.history.push("/");
  };

  const hideWorkouts = () => {
    props.hideWorkouts();
    props.history.push("/");
  };

  if (props.hiddenSettings) {
    return  (
      <div className={styles.row}>
        <div
          className={styles.hamburger}
          onClick={() => props.hideSettings()}
        >
          |||
        </div>
        <Link to="/">
        <div
          className={styles.logo}
          onClick={() => props.goHome()}
          tabIndex="0"
        >
          Exercise.it!
        </div>
        </Link>
      </div>
  )}

    return (
      <div className={styles.settings}>
      <div>
      <div className={styles.row}>
      <div
            className={styles.hamburger}
            onClick={() => props.hideSettings()}
          >
            |||
          </div>
        <Link to="/">
          <div
            className={styles.logo}
            onClick={() => props.goHome()}
            tabIndex="0"
          >
            Exercise.it!
          </div>
        </Link>
        </div>
          <div className={styles.rowSpace}>
            <div
              onClick={() => hideExercises()}
              className={
                props.hiddenExercises
                  ? styles.smallToggleTrue
                  : styles.smallToggleFalse
              }
            >
              Kun økter
            </div>
            <div
              onClick={() => hideWorkouts()}
              className={
                props.hiddenWorkouts
                  ? styles.smallToggleTrue
                  : styles.smallToggleFalse
              }
            >
              Kun øvelser
            </div>{" "}
          </div>
      </div>
      <div>
      {props.user && props.user.username ? (
        <Link to={`/userpage/${props.user ? props.user.username : ''}`}>
            <div
              className={
                window.location.href.indexOf(`userpage/${props.user.username}`) > -1
                  ? styles.settingActive
                  : styles.setting
              }
            >
              Min profil
            </div>
          </Link>
        ) : null}
          <div>
            <div
              onClick={() => newExercise()}
              className={
                props.creatingNewExercise
                  ? styles.settingActive
                  : styles.setting
              }
            >
              Legg til øvelse <strong className={styles.plus}>+</strong>
            </div>
            <div
              onClick={() => newWorkout()}
              className={
                props.creatingNewWorkout ? styles.settingActive : styles.setting
              }
            >
              Opprett økt <strong className={styles.plus}>+</strong>
            </div>{" "}
          </div>
        {props.user && props.user.username === "admin" ? (
          <a target="_self" href={url}>
            <div className={styles.setting}>Django-Admin</div>
          </a>
        ) : (
          <Link to="/info">
            <div
              className={
                window.location.href.indexOf("info") > -1
                  ? styles.settingActive
                  : styles.setting
              }
            >
              {" "}
              Informasjon
            </div>
          </Link>
        )}
        <Link to="/login">
          <div className={styles.loginSetting} onClick={() => props.login()}>
            {props.user && props.user.username ? "Logg ut" : "Logg inn"}
          </div>{" "}
        </Link>
      </div>
    </div>
  )
};

export default withRouter(Settings);
