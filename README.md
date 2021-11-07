# research_track_python

This package implements a solution to a simple simulated problem using the portable robot simulator developed by [Student Robotics](https://studentrobotics.org).

To run the python executable you can use the command  __python2 run.py assignment.py__ or __python2 run.py assignment_generalized.py__ 

## Executables 

**assignment.py** implements a specific solution for the problem using hard coded parameters.

**assignment_generalized.py** can be changed and used with different sets of parameters, to be adapted to any kind of similar simulation.


## Simulated Environment


In the simulated environment : 
- golden boxes represent walls to avoid
- silver boxes are scattered along the path

## Main goals 

The robot has to :

- constrantly drive around the circuit in the counter-clockwise direction
- avoid touching the golden boxes
- when the robot is close to a silver box, it should grab it, and move it behind its
    

## Main Functions

- Straight drive : drives the robot as straight as possible inside corridors.

- Detect front wall and turn : detects the distance to the wall in front of the robot, and if it is close enough makes the robot turn in the right direction to follow the path.

- Grab silver : detects the nearest silver token in front of the robot, and if it is close enough drives the robot to grab it and put it behind.


## Code Flowchart

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBBW1JPQk9UXSAtLT58RHJpdmUgaW4gY29ycmlkb3JzfCBCe1N0cmFpZ2h0IERyaXZlIEZ1bmN0aW9ufVxuICAgIEEgLS0-IHx0dXJuIGF0IGNvcm5lcnN8SntEZXRlY3Qgd2FsbCBhbmQgdHVybiBGdW5jdGlvbn1cbiAgICBBIC0tPiB8Z3JhYiBzaWx2ZXIgdG9rZW5zIGFsb25nIHRoZSBwYXRofEh7R3JhYiBTaWx2ZXIgRnVuY3Rpb259XG4gICAgQiAtLT4gQ1tEZXRlY3QgZGlzdGFuY2UgZnJvbSBsZWZ0IGFuZCByaWdodCB3YWxsc11cbiAgICBDIC0tPnxMZWZ0IHdhbGwgaXMgY2xvc2VyfCBEW1R1cm4gcmlnaHQgNSBkZWdyZWVzIGFuZCBkcml2ZSBmb3J3YXJkXVxuICAgIEMgLS0-fFJpZ2h0IHdhbGwgaXMgY2xvc2VyfCBFW1R1cm4gbGVmdCA1IGRlZ3JlZXMgYW5kIGRyaXZlIGZvcndhcmRdXG4gICAgQyAtLT58Qm90aCB3YWxsIGF0IHNhbWUgZGlzdGFuY2Ugb3IgZXJyb3IgaW4gZGV0ZWN0aW9ufCBGW0RyaXZlIGZvcndhcmRdXG4gICAgSiAtLT58RnJvbnQgV2FsbCBpcyBmYXIgYXdheXxLW0RyaXZlIGZvcndhcmRdIFxuICAgIEogLS0-fEZyb250IFdhbGwgaXMgY2xvc2UgZW5vdWdofExbRGV0ZWN0IGRpc3RhbmNlIGZyb20gbGVmdCBhbmQgcmlnaHQgd2FsbHNdXG4gICAgTCAtLT58TGVmdCB3YWxsIGlzIGNsb3NlcnxNW1R1cm4gUmlnaHQgOTAgZGVncmVlc11cbiAgICBMIC0tPnxSaWdodCB3YWxsIGlzIGNsb3NlcnxPW1R1cm4gTGVmdCA5MCBkZWdyZWVzXVxuICAgIEwgLS0-fEJvdGggd2FsbHMgYXQgc2FtZSBkaXN0YW5jZSBvciBlcnJvcnxOW0RyaXZlIEZvcndhcmQgYSBiaXRdICBcbiAgICBIIC0tPlZbRGV0ZWN0IGNsb3Nlc3Qgc2lsdmVyIHRva2VuIGluIGZyb250IG9mIHRoZSBSb2JvdF1cbiAgICBWIC0tPiB8dG9rZW4gaXMgY2xvc2UgZW5vdWdofFNbT3JpZW50YXRlIHRoZSByb2JvdCBhbmQgZHJpdmUgdG93YXJkcyB0aGUgdG9rZW5dXG4gICAgUyAtLT4gUltHcmFiIHRoZSB0b2tlbiBhbmQgcHV0IGl0IGJlaGluZCB0aGUgcm9ib3RdXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggVERcbiAgICBBW1JPQk9UXSAtLT58RHJpdmUgaW4gY29ycmlkb3JzfCBCe1N0cmFpZ2h0IERyaXZlIEZ1bmN0aW9ufVxuICAgIEEgLS0-IHx0dXJuIGF0IGNvcm5lcnN8SntEZXRlY3Qgd2FsbCBhbmQgdHVybiBGdW5jdGlvbn1cbiAgICBBIC0tPiB8Z3JhYiBzaWx2ZXIgdG9rZW5zIGFsb25nIHRoZSBwYXRofEh7R3JhYiBTaWx2ZXIgRnVuY3Rpb259XG4gICAgQiAtLT4gQ1tEZXRlY3QgZGlzdGFuY2UgZnJvbSBsZWZ0IGFuZCByaWdodCB3YWxsc11cbiAgICBDIC0tPnxMZWZ0IHdhbGwgaXMgY2xvc2VyfCBEW1R1cm4gcmlnaHQgNSBkZWdyZWVzIGFuZCBkcml2ZSBmb3J3YXJkXVxuICAgIEMgLS0-fFJpZ2h0IHdhbGwgaXMgY2xvc2VyfCBFW1R1cm4gbGVmdCA1IGRlZ3JlZXMgYW5kIGRyaXZlIGZvcndhcmRdXG4gICAgQyAtLT58Qm90aCB3YWxsIGF0IHNhbWUgZGlzdGFuY2Ugb3IgZXJyb3IgaW4gZGV0ZWN0aW9ufCBGW0RyaXZlIGZvcndhcmRdXG4gICAgSiAtLT58RnJvbnQgV2FsbCBpcyBmYXIgYXdheXxLW0RyaXZlIGZvcndhcmRdIFxuICAgIEogLS0-fEZyb250IFdhbGwgaXMgY2xvc2UgZW5vdWdofExbRGV0ZWN0IGRpc3RhbmNlIGZyb20gbGVmdCBhbmQgcmlnaHQgd2FsbHNdXG4gICAgTCAtLT58TGVmdCB3YWxsIGlzIGNsb3NlcnxNW1R1cm4gUmlnaHQgOTAgZGVncmVlc11cbiAgICBMIC0tPnxSaWdodCB3YWxsIGlzIGNsb3NlcnxPW1R1cm4gTGVmdCA5MCBkZWdyZWVzXVxuICAgIEwgLS0-fEJvdGggd2FsbHMgYXQgc2FtZSBkaXN0YW5jZSBvciBlcnJvcnxOW0RyaXZlIEZvcndhcmQgYSBiaXRdICBcbiAgICBIIC0tPlZbRGV0ZWN0IGNsb3Nlc3Qgc2lsdmVyIHRva2VuIGluIGZyb250IG9mIHRoZSBSb2JvdF1cbiAgICBWIC0tPiB8dG9rZW4gaXMgY2xvc2UgZW5vdWdofFNbT3JpZW50YXRlIHRoZSByb2JvdCBhbmQgZHJpdmUgdG93YXJkcyB0aGUgdG9rZW5dXG4gICAgUyAtLT4gUltHcmFiIHRoZSB0b2tlbiBhbmQgcHV0IGl0IGJlaGluZCB0aGUgcm9ib3RdXG4iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGVmYXVsdFwiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

## Possible improvements on current code 

If you want to use this code with another simulation in the same fashion, you can use the **assignment_generalized.py** file and tune the different parameters. The parameters are the following :

- front wall detection distance
- silver detection distance
- failsafe roation angle
- silver tolerance  
- front tolerance
- right/left tolerance

If the robot enters a corner with a certain angle, it can sometimes turn around.
This almost never happens but is still a possible case. In the case this happens in your simulation, retuning the front wall detection distance or the failsafe rotation angle should work fine.