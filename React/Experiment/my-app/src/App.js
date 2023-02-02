import React, { useState } from 'react';
import './ResumeBuilder.css';
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';
pdfMake.vfs = pdfFonts.pdfMake.vfs;

function ResumeBuilder() {
  const [name, setName] = useState('');
  const [experience, setExperience] = useState([{
    company: '',
    role: '',
    startYear: '',
    endYear: '',
    responsibilities: ''
  }]);
  const [skills, setSkills] = useState('');
  const [education, setEducation] = useState('');

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleExperienceChange = (event, index) => {
    const newExperience = [...experience];
    newExperience[index][event.target.name] = event.target.value;
    setExperience(newExperience);
  };
  const handleSkillsChange = (event) => {
    setSkills(event.target.value);
  };
  const handleEducationChange = (event) => {
    setEducation(event.target.value);
  };
  const addExperience = () => {
    setExperience([...experience, {
      company: '',
      role: '',
      startYear: '',
      endYear: '',
      responsibilities: ''
    }]);
  };
  const removeExperience = (index) => {
    const newExperience = [...experience];
    newExperience.splice(index, 1);
    setExperience(newExperience);
  };
  const handleDownload = () => {
    const docDefinition = {
      content: [
        {text: name, style: 'name'},
        {text: 'Work Experience:', style: 'subheader'},
				...experience.map(exp => {
						return [
								{text: exp.company, bold: true, fontSize: 14},
								{text: exp.role,  fontSize: 12},
								{text: `${exp.startYear} - ${exp.endYear}`, fontSize: 10},
								{text: exp.responsibilities, fontSize: 11, color: '#666666'}
						];
				}),
        {text: 'Education:', style: 'subheader'},
        {text: education, style: 'text'},
        {text: 'Skills:', style: 'subheader'},
        {text: skills, style: 'text', fontSize: 11, color: '#666666'},
      ],
      styles: {
        header: {
          fontSize: 18,
          bold: true,
          margin: [0, 0, 0, 10],
        },
        subheader: {
          fontSize: 14,
          bold: true,
          margin: [0, 15, 0, 5],
        },
        name: {
          fontSize: 16,
          bold: true,
          margin: [0, 5, 0, 0]
        },
        text: {
          fontSize: 12,
          margin: [0, 5, 0, 0]
        },
				list: {
					fontSize: 10,
					margin: [0, 5, 0, 0]
				}
      },
      // Add more styling here
    };
    pdfMake.createPdf(docDefinition).download(`${name}-resume.pdf`);
  };
  return (
    <div>
      <h1>Resume Builder</h1>
      <form>
        <label>
          Name:
          <input type="text" value={name} onChange={handleNameChange} />
        </label>
        <br />
        <br />
        <label>
          Experience:
          {experience.map((exp, index) => {
            return (
              <div key={index}>
                <input type="text" name="company" value={exp.company} placeholder="Company" onChange={(event) => handleExperienceChange(event, index)} />
                <input type="text" name="role" value={exp.role} placeholder="Role" onChange={(event) => handleExperienceChange(event, index)} />
                <input type="text" name="startYear" value={exp.startYear} placeholder="Start Year" onChange={(event) => handleExperienceChange(event, index)} />
                <input type="text" name="endYear" value={exp.endYear} placeholder="End Year" onChange={(event) => handleExperienceChange(event, index)} />
                <input type="text" name="responsibilities" value={exp.responsibilities} placeholder="Responsibilities" onChange={(event) => handleExperienceChange(event, index)} />
                <button type="button" onClick={() => removeExperience(index)}>Remove</button>
              </div>
            );
          })}
          <button type="button" onClick={addExperience}>Add</button>
        </label>
        <br />
        <br />
        <label>
          Skills:
          <textarea value={skills} onChange={handleSkillsChange} />
        </label>
        <br />
        <br />
        <label>
          Education:
          <textarea value={education} onChange={handleEducationChange} />
        </label>
        <br />
        <br />
      </form>
      <h2>Preview</h2>

      <div>
        <h3>{name}</h3>
        <p>Experience:</p>
        {experience.map((exp, index) => {
            return (
              <div key={index}>
                <p>Company: {exp.company}</p>
                <p>Role: {exp.role}</p>
                <p>Start Year: {exp.startYear}</p>
                <p>End Year: {exp.endYear}</p>
                <p>Responsibilities: {exp.responsibilities}</p>
              </div>
            );
          })}
        <p>Education:</p>
        <p>{education}</p>
        <p>Skills:</p>
        <p>{skills}</p>

      </div>
      <button onClick={handleDownload}>Download PDF</button>

    </div>
  );
}

export default ResumeBuilder;