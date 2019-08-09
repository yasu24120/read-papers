# Textual Explanations for Self-Driving Vehicles
http://openaccess.thecvf.com/content_ECCV_2018/papers/Jinkyu_Kim_Textual_Explanations_for_ECCV_2018_paper.pdf
(コード (tensorflow))  
https://github.com/JinkyuKimUCB/explainable-deep-driving

## 概要 

User acceptance is likely to benefit from easyto-interpret textual explanations which allow end-users to understand what triggered a particular behavior. Explanations may be triggered by the neural controller, namely introspective explanations, or informed by the neural controller’s
output, namely rationalizations. We propose a new approach to introspective explanations which consists of two parts. First, we use a visual (spatial) attention
model to train a convolutional network end-to-end from images to the vehicle
control commands, i.e., acceleration and change of course. The controller’s attention identifies image regions that potentially influence the network’s output.
Second, we use an attention-based video-to-text model to produce textual explanations of model actions. The attention maps of controller and explanation
model are aligned so that explanations are grounded in the parts of the scene that
mattered to the controller. We explore two approaches to attention alignment,
strong- and weak-alignment. Finally, we explore a version of our model that
generates rationalizations, and compare with introspective explanations on the
same video segments

## Contributions

## 本文メモ

### 前提知識
Explainable models that make deep models more transparent are important for a number of
reasons: (i) user acceptance – self-driving vehicles are a radical technology for users
to accept, and require a very high level of trust, (ii) understanding and extrapolation of
vehicle behavior – users ideally should be able to anticipate what the vehicle will do
in most situations, (iii) effective communication – they help user communicate preferences to the vehicle and vice versa.

Explanations can be either rationalizations – explanations that justify the system’s
behavior in a post-hoc manner, or introspective explanations – explanations that are
based on the system’s internal state. Introspective explanations represent causal relationships between the system’s input and its behavior, and address all the goals above.
Rationalizations can address acceptance, (i) above, but are less helpful with (ii) understanding the causal behavior of the model or (iii) communication which is grounded in
the vehicle’s internal state (known as theory of mind in human communication).

One way of generating introspective explanations is via visual attention

Visual attention constrains the reasons for the controllers actions but does not e.g., tie specific actions to specific input regions e.g., “the
vehicle slowed down because the light controlling the intersection is red”. It is also
likely to be less convenient for passengers to replay the attention map vs. a (typically
on-demand) speech presentation of a textual explanation.


### 問題設定  
