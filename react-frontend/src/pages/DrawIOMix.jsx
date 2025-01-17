import React, { useEffect, useRef } from 'react';
import CORSCommunicator from './Draw_io/CORSCommunicator'
import DrawioStateController from './Draw_io/DrawioController.js'
import LocalStorageModel from './Draw_io/LocalStorageModel.js'
import './Draw_io/styles/style.css'
import './Draw_io/styles/variables.css'

import Paper from '@mui/material/Paper'

import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'

function DrawIO({ sendDiagram }) {
  const iframeRef = useRef(null);


  const initialized = useRef(false);
  useEffect(() => {
    if (!initialized.current) {
      var localStorageModel = new LocalStorageModel()
      try {
        var selectedModel = localStorage.getItem('selectedModel')
        var loaded = JSON.parse(localStorage.getItem('storedModels')) || []
      } catch (error) {
        loaded = []
      }
      var selectedStoreModel = loaded.find(m => m.id === selectedModel)
      if (selectedStoreModel.diagram) {
        localStorageModel.write(selectedStoreModel.diagram)
      } else {
        localStorage.removeItem('diagram')
      }

      initialized.current = true
      var drawioView = new CORSCommunicator(iframeRef.current)
      var stateController = new DrawioStateController(drawioView, localStorageModel)
      localStorageModel.observe(function(diagram) {
        sendDiagram(diagram)
        selectedStoreModel.diagram = diagram
        localStorage.setItem('storedModels', JSON.stringify(loaded))
      })
      sendDiagram(localStorageModel.read())
    }
  }, [sendDiagram]);

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h4">
        Architectural Modeling
      </Typography>
      <Typography
        variant="subtitle" sx={{ marginBottom: '1em' }}>
        Draw the architectural diagram
      </Typography>
      <Paper elevation={4} sx={{ width: '100%', height: '100%', borderRadius: '.5em', overflow: 'hidden' }}>
        <iframe
          ref={iframeRef}
          width="100%"
          height="100%"
          src="https://embed.diagrams.net/?embed=1&ui=dark&spin=1&proto=json&configure=1&noExitBtn=1&saveAndExit=0&noSaveBtn=1&noExitBtn=1"
          style={{ border: 'none' }}
          title={'draw.io'}
        />
      </Paper>
    </Box>

  );
}

export default DrawIO;
