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
      margin: theme.spacing(1), width: theme.spacing(16), height: theme.spacing(16),
    },
  },
}));

export default function DescriptionComp() {
  const classes = useStyles();

  const {getRootProps, getInputProps} = useDropzone()
  const {ref, ...rootProps} = getRootProps()

  return (
    <div className={classes.root}>

<RootRef rootRef={ref}>
    <Paper  {...rootProps}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop the video files here, or click to select the file</p>
        </Paper>
      </RootRef>
    </div>
  );
}