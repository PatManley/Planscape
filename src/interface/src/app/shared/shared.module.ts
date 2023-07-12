import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from 'src/app/material/material.module';

import { FileUploaderComponent } from './file-uploader/file-uploader.component';
import { OpacitySliderComponent } from './opacity-slider/opacity-slider.component';

@NgModule({
  declarations: [
    FileUploaderComponent,
    OpacitySliderComponent,
  ],
  exports: [FileUploaderComponent, OpacitySliderComponent],
  imports: [CommonModule, FormsModule, MaterialModule, ReactiveFormsModule],
})
export class SharedModule {}
