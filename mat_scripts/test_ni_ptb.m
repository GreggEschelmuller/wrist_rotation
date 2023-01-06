% Clear the workspace and the screen
sca;
close all;
clear;

dq = daq("ni");
dq.Rate = 500;
% Update device ID
addinput(dq, "cDAQ1Mod4", "ai0", "Voltage");
addinput(dq, "cDAQ1Mod4", "ai1", "Voltage");

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Seed the random number generator. Here we use the an older way to be
% compatible with older systems.
rng('shuffle');

% Get the screen numbers. This gives us a number for each of the screens
% attached to our computer.
screens = Screen('Screens');

% Draw we select the maximum of these numbers. So in a situation where we
% have two screens attached to our monitor we will draw to the external
% screen. When only one screen is attached to the monitor we will draw to
% this.
screenNumber = max(screens);

% Define black and white (white will be 1 and black 0).
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);

% Open an on screen window and color it black
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, black);

% Get the size of the on screen window in pixels
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window in pixels
[xCenter, yCenter] = RectCenter(windowRect);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Sync us and get a time stamp
vbl = Screen('Flip', window);
waitframes = 1;

% Maximum priority level
topPriorityLevel = MaxPriority(window);
Priority(topPriorityLevel);


dotColor = [1 0 0];
dotSizePix = 20;
counter = 0;
end_time = GetSecs + 1;
% Loop the animation until a key is pressed
while elapsed_time < end_time
    
    pos_data = read(dq, "OutputFormat", "Matrix");
    x = pos_data(1);
    y = pos_data(2);
    
    Screen('DrawDots', window, [x y], dotSizePix, dotColor, [], 2);
    
    % Flip to the screen
    vbl  = Screen('Flip', window);

    elapsed_time = GetSecs;
    counter = counter + 1;
end

sca;