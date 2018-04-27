import {BasicDataModel} from "./basic-data-model";
import {DetailedDataModel} from "./detailed-data-model";

export class CombinedDataModel {

  constructor(public basicData: BasicDataModel, public detailedData: DetailedDataModel) {
  }
}
