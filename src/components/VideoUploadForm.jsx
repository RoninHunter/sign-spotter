import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

import {useDropzone} from 'react-dropzone'
import RootRef from '@material-ui/core/RootRef'


const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    '& > *': {
      margin: theme.spacing(10), width: theme.spacing(80), height: theme.spacing(12),
    },
  },
}));

export default function VideoUploadForm() {
  const classes = useStyles();

  const {getRootProps, getInputProps} = useDropzone()
  const {ref, ...rootProps} = getRootProps()

  return (
    <div className={classes.root}>

<RootRef rootRef={ref}>
    <Paper {...rootProps}>
        <input {...getInputProps()} />
        <p> Upload video by drag 'n' dropping your video file or click to select the file</p>
        </Paper>
      </RootRef>
    </div>
  );
}